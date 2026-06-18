import os
import torch
import torchaudio

# ---------------------------------------------------------------------------
# Robust audio loader — works on Windows without FFmpeg DLLs.
# torchaudio 2.10.0 changed its default backend to torchcodec which requires
# FFmpeg full-shared DLLs. We bypass this by using soundfile directly.
# ---------------------------------------------------------------------------

def _load_audio(file_path: str):
    """
    Load audio file returning (waveform_tensor [channels, samples], sample_rate).

    Backend selection:
      - MP3/M4A/AAC/WEBM  →  pydub (calls system ffmpeg binary, no DLL issues)
      - WAV/FLAC/OGG/AIFF →  soundfile (fast, pure-Python, no ffmpeg needed)
      - Fallback           →  torchaudio with explicit soundfile backend

    This completely avoids torchaudio 2.10.0's new default torchcodec backend
    which requires FFmpeg full-shared DLLs on Windows.
    """
    import os
    ext = os.path.splitext(file_path)[1].lower()

    # --- MP3 / compressed formats: use pydub → ffmpeg binary ---
    if ext in ('.mp3', '.m4a', '.aac', '.webm', '.opus', '.wma', '.ogg'):
        try:
            from pydub import AudioSegment
            import numpy as np
            audio = AudioSegment.from_file(file_path)
            sr = audio.frame_rate
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            # Normalize to [-1.0, 1.0]
            samples /= float(1 << (audio.sample_width * 8 - 1))
            channels = audio.channels
            if channels > 1:
                samples = samples.reshape(-1, channels).T
            else:
                samples = samples.reshape(1, -1)
            wav = torch.from_numpy(samples)
            print(f"[Audio] Loaded via pydub — sr={sr}, shape={wav.shape}")
            return wav, sr
        except Exception as e_pydub:
            print(f"[Audio] pydub failed ({e_pydub}), trying soundfile fallback…")

    # --- WAV / FLAC / uncompressed: use soundfile ---
    try:
        import soundfile as sf
        import numpy as np
        data, sr = sf.read(file_path, dtype='float32', always_2d=True)
        # soundfile: (samples, channels) → torchaudio: (channels, samples)
        wav = torch.from_numpy(data.T)
        print(f"[Audio] Loaded via soundfile — sr={sr}, shape={wav.shape}")
        return wav, sr
    except Exception as e_sf:
        print(f"[Audio] soundfile failed ({e_sf}), trying torchaudio soundfile backend…")

    # --- Last resort: torchaudio with explicit soundfile backend ---
    try:
        wav, sr = torchaudio.load(file_path, backend="soundfile")
        print(f"[Audio] Loaded via torchaudio(soundfile) — sr={sr}, shape={wav.shape}")
        return wav, sr
    except Exception as e_ta:
        raise RuntimeError(
            f"Could not load audio '{file_path}'. All backends failed.\n"
            f"  pydub/ffmpeg: see above\n"
            f"  soundfile: {e_sf}\n"
            f"  torchaudio/soundfile: {e_ta}"
        )


def _save_audio(file_path: str, tensor: torch.Tensor, sample_rate: int):
    """
    Save audio tensor [channels, samples] to file_path.
    Uses soundfile directly (avoiding torchaudio's default torchcodec backend).
    """
    try:
        import soundfile as sf
        # soundfile expects (samples, channels)
        data = tensor.detach().cpu().numpy().T
        sf.write(file_path, data, sample_rate)
        print(f"[Audio] Saved via soundfile: {file_path}")
    except Exception as e:
        print(f"[Audio] soundfile save failed ({e}), trying torchaudio soundfile backend…")
        try:
            torchaudio.save(file_path, tensor, sample_rate, backend="soundfile")
            print(f"[Audio] Saved via torchaudio(soundfile): {file_path}")
        except Exception as e_ta:
            raise RuntimeError(
                f"Could not save audio '{file_path}'. All backends failed.\n"
                f"  soundfile: {e}\n"
                f"  torchaudio/soundfile: {e_ta}"
            )


# ---------------------------------------------------------------------------
# Module-level model cache  { model_name: demucs_model }
# The model is loaded the first time it is requested, then kept in memory so
# subsequent calls reuse the same weights without any re-loading overhead.
# ---------------------------------------------------------------------------
_model_cache: dict = {}


def _get_device() -> str:
    """Detect best available device: cuda > mps > cpu"""
    if torch.cuda.is_available():
        return 'cuda'
    if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return 'mps'
    return 'cpu'


def _load_model(model_name: str = 'htdemucs'):
    """
    Return the requested Demucs model, loading it only on the first call.
    Subsequent calls with the same name return the cached instance instantly.
    """
    if model_name in _model_cache:
        print(f"[Demucs] Model '{model_name}' loaded from cache.")
        return _model_cache[model_name]

    print(f"[Demucs] Loading model '{model_name}' for the first time — this may take a moment...")
    from demucs.pretrained import get_model

    device = _get_device()
    model = get_model(model_name)
    model.to(device)
    model.eval()

    _model_cache[model_name] = model
    print(f"[Demucs] Model '{model_name}' loaded and cached on {device}.")
    return model


def separate_audio(file_path, model='htdemucs', output_folder='separated', two_stems=None):
    """
    Separate audio into stems using the Demucs Python API.

    The model is loaded once and kept in a module-level cache; every call
    after the first reuses the cached weights.

    Args:
        file_path:     Path to the audio file to separate.
        model:         Demucs model name (htdemucs, htdemucs_ft, htdemucs_6s, …).
        output_folder: Root folder to write separated stems into.
        two_stems:     If set (e.g. 'vocals'), save only that stem plus the
                       combined remainder ('no_<stem>').

    Returns:
        Path to the stems folder on success, None on failure.
        Structure: output_folder/model_name/track_name/{stem}.wav
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        device = _get_device()

        print(f"[Demucs] Input file  : {file_path}")
        print(f"[Demucs] Output root : {output_folder}")
        print(f"[Demucs] Model       : {model}")
        print(f"[Demucs] Device      : {device}")

        # ── 1. Load / retrieve the cached model ────────────────────────────
        demucs_model = _load_model(model)

        # ── 2. Load audio and convert to model's expected format ───────────
        from demucs.audio import convert_audio
        from demucs.apply import apply_model

        wav, sr = _load_audio(file_path)
        wav = convert_audio(wav, sr, demucs_model.samplerate, demucs_model.audio_channels)
        wav = wav.to(device)

        # ── 3. Run separation ───────────────────────────────────────────────
        print("[Demucs] Running separation…")
        with torch.no_grad():
            # apply_model expects a batch dimension → [1, channels, samples]
            sources = apply_model(demucs_model, wav[None], device=device, progress=True)[0]

        sources = sources.cpu()
        stem_names = demucs_model.sources   # e.g. ['drums', 'bass', 'other', 'vocals']

        # ── 4. Save stems ───────────────────────────────────────────────────
        track_name = os.path.splitext(os.path.basename(file_path))[0]
        stems_path = os.path.join(output_folder, model, track_name)
        os.makedirs(stems_path, exist_ok=True)

        if two_stems:
            # Save the requested stem and a combined "no_<stem>" track
            target_idx = stem_names.index(two_stems) if two_stems in stem_names else None
            for idx, (name, source) in enumerate(zip(stem_names, sources)):
                if target_idx is None:
                    # Stem not found — save all
                    out_name = f"{name}.wav"
                elif idx == target_idx:
                    out_name = f"{name}.wav"
                else:
                    continue   # skip individual non-target stems

                out_path = os.path.join(stems_path, out_name)
                _save_audio(out_path, source, demucs_model.samplerate)
                print(f"[Demucs] Saved {out_name}")

            # Build the combined remainder track
            if target_idx is not None:
                others = [s for i, s in enumerate(sources) if i != target_idx]
                if others:
                    combined = torch.stack(others).sum(dim=0)
                    no_stem_path = os.path.join(stems_path, f"no_{two_stems}.wav")
                    _save_audio(no_stem_path, combined, demucs_model.samplerate)
                    print(f"[Demucs] Saved no_{two_stems}.wav")
        else:
            for name, source in zip(stem_names, sources):
                out_path = os.path.join(stems_path, f"{name}.wav")
                _save_audio(out_path, source, demucs_model.samplerate)
                print(f"[Demucs] Saved {name}.wav")

        print(f"[Demucs] Separation complete — stems in: {stems_path}")
        print(f"[Demucs] Files: {os.listdir(stems_path)}")
        return stems_path

    except Exception as e:
        print(f"[Demucs] Error during separation: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_available_models():
    """Return the list of supported Demucs model names."""
    return [
        'htdemucs',       # Hybrid Transformer Demucs (4 stems: vocals, drums, bass, other)
        'htdemucs_ft',    # Fine-tuned version
        'htdemucs_6s',    # 6 stems version (adds piano and guitar)
        'mdx_extra',      # MDX model
        'mdx_extra_q',    # Quantized MDX model (faster, lower quality)
    ]


def check_demucs_installed():
    """Return True if the demucs package can be imported."""
    try:
        import demucs  # noqa: F401
        return True
    except ImportError:
        return False

