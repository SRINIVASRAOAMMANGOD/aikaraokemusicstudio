# 🚀 Hugging Face Spaces Deployment Guide

**AI Karaoke Music Studio** - Complete deployment guide for Hugging Face Spaces

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Quick Start (5 minutes)](#quick-start-5-minutes)
3. [Detailed Setup Steps](#detailed-setup-steps)
4. [Configuration](#configuration)
5. [Testing & Verification](#testing--verification)
6. [Troubleshooting](#troubleshooting)
7. [Advanced](#advanced)

---

## Prerequisites

### Required
- **Hugging Face Account** (free): https://huggingface.co/join
- **GitHub Repository** (already ready): Your forked/cloned repo
- **Git** installed on your machine
- **Terminal/PowerShell** access

### Recommended
- Basic understanding of Docker
- Familiarity with environment variables
- Access to generate secure keys

---

## Quick Start (5 minutes)

```bash
# 1. Create HF Space (Docker SDK)
# Go to: https://huggingface.co/spaces → New Space
# Name: ai-karaoke-studio, SDK: Docker, Visibility: Public

# 2. Get your HF API token
# https://huggingface.co/settings/tokens → New token (role: write)

# 3. Clone and push code (in terminal)
git clone https://huggingface.co/spaces/{YOUR-HF-USERNAME}/ai-karaoke-studio
cd ai-karaoke-studio
git remote add github https://github.com/{YOUR-GITHUB}/{YOUR-REPO}.git
git pull github main --allow-unrelated-histories
git push origin main  # Password = your HF API token

# 4. Set environment variables
# Go to Space Settings → Repository secrets, add:
# - FLASK_ENV = production
# - SECRET_KEY = (generate: python3 -c "import secrets; print(secrets.token_hex(16))")
# - TORCH_NUM_THREADS = 2

# 5. Wait for build (~3-5 min)
# Check Space → Logs tab

# 6. Test
# Go to Space URL → Upload audio → Verify stem separation works

# 7. Share
# Your portfolio link: https://huggingface.co/spaces/{your-username}/ai-karaoke-studio
```

---

## Detailed Setup Steps

### Step 1: Create Hugging Face Account

1. Go to https://huggingface.co/join
2. Sign up (email or GitHub)
3. Verify email
4. Complete profile

**Status**: ✅ Account ready

---

### Step 2: Create API Token

1. Visit https://huggingface.co/settings/tokens
2. Click "New token"
3. Fill in:
   - **Token name**: `hf_spaces_deploy`
   - **Role**: `write`
4. Click "Create token"
5. **Copy the token** (you won't see it again)
6. Save securely in a notepad temporarily

**Status**: ✅ Token obtained

---

### Step 3: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in form:
   - **Space name**: `ai-karaoke-studio`
   - **License**: `apache-2.0` (or your preferred license)
   - **Space SDK**: `Docker` ⭐ **MUST BE DOCKER**
   - **Visibility**: `Public`
4. Click "Create Space"

**Result**: You get a URL like:
```
https://huggingface.co/spaces/{your-username}/ai-karaoke-studio
```

Save this URL.

**Status**: ✅ Space created

---

### Step 4: Push Your Code

Open **PowerShell** or **Git Bash**:

```bash
# Navigate to your workspace
cd c:\Users\HP\Desktop\deployment

# Clone the empty HF Space repo
git clone https://huggingface.co/spaces/{YOUR-HF-USERNAME}/ai-karaoke-studio
cd ai-karaoke-studio
```

**Replace `{YOUR-HF-USERNAME}` with your actual HF username**

Then:
```bash
# Add your GitHub repo as a remote
git remote add github https://github.com/{YOUR-GITHUB-USERNAME}/{YOUR-REPO-NAME}.git

# Fetch from GitHub (allow unrelated histories)
git pull github main --allow-unrelated-histories

# Push to HF Space
git push origin main
```

**When prompted for credentials**:
- **Username**: Your HF username
- **Password**: Paste the API token (not your HF password!)

**Status**: ✅ Code pushed to HF

---

### Step 5: Verify Dockerfile Configuration

The Dockerfile has been updated for HF Spaces:
- ✅ Port set to **7860** (HF requirement)
- ✅ Workers set to **2** (optimized for HF shared resources)
- ✅ Multi-stage build (optimized image size)
- ✅ Non-root user (security best practice)

**No changes needed** - already done! ✅

---

### Step 6: Set Environment Variables

1. Go to your HF Space URL
2. Click "Settings" tab
3. Scroll to "Repository secrets"
4. Click "New secret" and add each:

#### Secret 1: FLASK_ENV
```
Name:  FLASK_ENV
Value: production
```

#### Secret 2: SECRET_KEY
Generate a secure key (run in terminal):
```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```
This outputs a 32-character random string. Copy it.

```
Name:  SECRET_KEY
Value: [paste the generated key here]
```

#### Secret 3: TORCH_NUM_THREADS
```
Name:  TORCH_NUM_THREADS
Value: 2
```

#### Secret 4: DEMUCS_MODEL
```
Name:  DEMUCS_MODEL
Value: htdemucs
```

#### Secret 5: ENABLE_YOUTUBE_DOWNLOAD
```
Name:  ENABLE_YOUTUBE_DOWNLOAD
Value: true
```

After adding each secret, HF will automatically trigger a rebuild.

**Status**: ✅ Secrets configured

---

### Step 7: Monitor the Build

1. Go to your Space → "Logs" tab
2. Watch the build progress
3. Should show:
   ```
   ✓ Building Docker image...
   ✓ Installing dependencies...
   ✓ Pushing image...
   ✓ Space is running
   ```

**Build time**: ~3-5 minutes (first time)

**If build fails**:
- Check Logs for error message
- Common fixes:
  - Missing system dependency → add to `apt-get install` in Dockerfile
  - Python package conflict → update `requirements.txt`
  - Memory exceeded → check logs for OOM errors
- Fix and commit → HF rebuilds automatically

**Status**: ✅ Build complete

---

### Step 8: Test Your Deployment

1. Go to your Space URL
2. Wait for app to load (~10 seconds)
3. You should see the AI Karaoke homepage

**Test Workflow**:
```
1. Upload an audio file (MP3, WAV, FLAC, OGG, M4A, AAC)
   → First upload: ~30-60 seconds (Demucs model downloads)
   
2. Wait for stem separation
   → Shows separated stems (vocals, bass, drums, etc.)
   
3. Try recording/scoring (optional)
   → Should work if model cached
   
4. Upload another file
   → Should be ~30-40 seconds (faster - model cached)
```

**Status**: ✅ App tested and verified

---

## Configuration

### Environment Variables Reference

| Variable | Value | Purpose | Required |
|----------|-------|---------|----------|
| `FLASK_ENV` | `production` | Production mode | ✅ Yes |
| `SECRET_KEY` | 32-char random | Flask session encryption | ✅ Yes |
| `TORCH_NUM_THREADS` | `2` | CPU thread optimization | ✅ Yes |
| `DEMUCS_MODEL` | `htdemucs` | Default stem separation model | ❌ No (default) |
| `ENABLE_YOUTUBE_DOWNLOAD` | `true` | Allow YouTube URLs | ❌ No (default) |
| `ENABLE_AI_ANALYSIS` | `true` | Enable vocal scoring | ❌ No (default) |
| `LOG_LEVEL` | `info` | Logging verbosity | ❌ No (default) |

### Available Demucs Models

- `htdemucs` ⭐ **Default** - Balanced quality/speed
- `htdemucs_ft` - Fine-tuned variant
- `htdemucs_6s` - 6-stem (no piano/guitar)
- `mdx_extra` - Extra quality (slower)
- `mdx_extra_q` - Quantized (faster)

---

## Testing & Verification

### Quick Test Checklist

- [ ] Space URL accessible
- [ ] Homepage loads without errors
- [ ] Can upload audio file
- [ ] Stem separation starts
- [ ] Model downloads on first request (show progress)
- [ ] Separation completes
- [ ] Results display (stems visible)
- [ ] Second upload faster (model cached)

### Performance Baseline

| Operation | Time | Notes |
|-----------|------|-------|
| Page load | <2s | After first request |
| Model download | ~30-60s | Only on first upload |
| Stem separation | ~60-120s | Depending on audio length |
| Cached inference | ~30-40s | After model cached |

### Debug Logs

Check logs for issues:
1. Go to Space → "Logs" tab
2. Watch for errors during operation
3. Common messages:
   ```
   [Startup] Pre-warming Demucs model 'htdemucs'...
   [Startup] Model 'htdemucs' ready — first upload will be instant.
   [Processing] Starting stem separation...
   [Processing] Separation complete in X seconds
   ```

---

## Troubleshooting

### Issue: Build Fails with "ModuleNotFoundError"

**Error**:
```
ModuleNotFoundError: No module named 'xyz'
```

**Solution**:
1. Add package to `requirements.txt`
2. Commit and push
3. HF rebuilds automatically

```bash
git add requirements.txt
git commit -m "Add missing dependency: xyz"
git push origin main
```

---

### Issue: App Won't Start / Port Error

**Error**:
```
Address already in use: ('0.0.0.0', 5000)
```

**Solution**:
- Ensure Dockerfile has `EXPOSE 7860` (not 5000)
- Ensure `--bind 0.0.0.0:7860` (not 5000)
- Already fixed in this repo ✅

**To restart Space**:
1. Go to Settings
2. Scroll down → "Restart space"
3. Click "Restart"

---

### Issue: First Upload Takes Too Long

**Error**:
```
504 Gateway Timeout
```

**Why**: Demucs model (~500MB) is downloading on first request

**Solution**:
- This is normal - first upload takes 30-60 seconds
- Increase timeout if needed:
  ```dockerfile
  --timeout 300  # Increase to 300s if needed
  ```

---

### Issue: Uploads Disappear / Storage Lost

**Why**: HF Spaces storage is ephemeral (~50GB temporary)

**Expected behavior**:
- App auto-cleanup deletes projects >7 days old
- This is intentional to stay within storage quota
- Database persists within container session

**If you need persistent storage**:
- Contact HF team for persistent storage option
- Or use a different platform (Oracle Cloud, AWS)

---

### Issue: Model Never Finishes Downloading

**Diagnosis**:
1. Check Space Logs for errors
2. Verify internet connection is stable
3. Model file is large (~500MB)

**Solution**:
- Wait longer (give it 2-3 minutes)
- Restart Space and try again
- Check disk space in Logs

---

### Issue: Out of Memory (OOM)

**Error**:
```
Killed: Torch process terminated due to OOM
```

**Why**: Demucs needs ~2-4GB RAM per request

**Solution**:
- HF Spaces allocates based on availability
- Request GPU tier (provides more resources)
- Or use simpler model: `mdx_extra_q` (quantized)

---

## Advanced

### Updating Code After Deployment

To push updates to your deployed Space:

```bash
# Make changes locally
# Edit files, test locally

# Push to GitHub
git add .
git commit -m "Feature: description of changes"
git push github main

# Push to HF Space (in HF Space local directory)
git pull github main
git push origin main

# HF auto-rebuilds on push
```

---

### Using Custom Models

To use a different Demucs model:

1. Go to Space Settings → Repository secrets
2. Change `DEMUCS_MODEL` to desired model:
   - `htdemucs_ft`
   - `htdemucs_6s`
   - `mdx_extra`
   - `mdx_extra_q`
3. Recommit or trigger rebuild
4. First request will download new model

---

### Enabling GPU (If Available)

GPU speeds up Demucs 5-10x:

1. Go to Space Settings
2. Look for "Hardware" section
3. Select GPU option (if available)
4. Space will restart with GPU
5. Demucs will auto-detect and use GPU

---

### Monitoring & Logs

**Real-time Logs**:
- Space → Logs tab
- Shows all container output

**Common Log Messages**:
```
[Startup] Pre-warming Demucs model...   → Loading model at startup
[Health] /health endpoint called          → Server is alive
[Processing] Starting stem separation     → Audio processing started
[Error] Torch CUDA device not available   → GPU not found (falls back to CPU)
```

---

### Backing Up Your Database

To backup your karaoke projects:

1. Go to Space → Files tab
2. Download `karaoke_studio.db`
3. Store safely
4. Can be restored by uploading to new Space

---

### Scaling to Production

If you get many users:

1. **Switch to Oracle Cloud Always Free** (free indefinitely)
2. **Use AWS** (if budget allows)
3. **Contact HF** for enterprise tier

---

## Portfolio Presentation

### Share Your Link

```
https://huggingface.co/spaces/{your-username}/ai-karaoke-studio
```

### GitHub Integration

Add to your portfolio:
```markdown
## AI Karaoke Music Studio
**Live Demo**: [HF Spaces](https://huggingface.co/spaces/{your-username}/ai-karaoke-studio)

- Stem separation using Demucs 4.0
- Vocal karaoke recording & playback
- AI performance scoring (pitch, timing, tone)
- Built with Flask, PyTorch, Librosa
- Deployed on Hugging Face Spaces

**Features**:
- Real-time audio processing
- Multi-stem mixing
- YouTube URL support
- AI-powered analysis
```

---

## Support & Help

**For HF Spaces issues**: https://huggingface.co/docs/hub/spaces

**For PyTorch/Demucs issues**: 
- https://github.com/facebookresearch/demucs
- https://pytorch.org/docs/

**For Flask/Web issues**:
- https://flask.palletsprojects.com/
- Check Space logs for error details

---

## Checklist: Deployment Complete ✅

- [ ] HF account created
- [ ] API token generated
- [ ] Space created (Docker SDK)
- [ ] Code pushed to HF
- [ ] Dockerfile port = 7860 ✅
- [ ] Environment variables set
- [ ] Build completed (no errors)
- [ ] App loaded successfully
- [ ] Test upload successful
- [ ] Model cached on 2nd upload
- [ ] Link added to portfolio
- [ ] Ready for recruitment! 🎉

---

**Deployment Status**: ✅ READY FOR PRODUCTION

Your AI Karaoke Music Studio is now live on Hugging Face Spaces!

🔗 **Share this link**: https://huggingface.co/spaces/{your-username}/ai-karaoke-studio
