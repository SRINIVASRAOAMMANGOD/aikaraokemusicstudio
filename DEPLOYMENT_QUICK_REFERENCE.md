# DEPLOYMENT QUICK REFERENCE - AI Karaoke Music Studio

## 📋 5-Minute Deployment Summary

```bash
# 1. Create HF Space (Docker SDK)
# Go: https://huggingface.co/spaces → New Space
# Name: ai-karaoke-studio

# 2. Get API token
# Go: https://huggingface.co/settings/tokens → New token

# 3. Push code
git clone https://huggingface.co/spaces/{HF-USERNAME}/ai-karaoke-studio
cd ai-karaoke-studio
git remote add github https://github.com/{GITHUB-USERNAME}/{REPO}.git
git pull github main --allow-unrelated-histories
git push origin main  # Use HF API token as password

# 4. Set secrets (HF Space Settings → Repository secrets)
FLASK_ENV = production
SECRET_KEY = python3 -c "import secrets; print(secrets.token_hex(16))"
TORCH_NUM_THREADS = 2
DEMUCS_MODEL = htdemucs
ENABLE_YOUTUBE_DOWNLOAD = true

# 5. Wait for build (check Logs tab: ~3-5 min)

# 6. Test: Go to Space URL and upload audio

# 7. Share: https://huggingface.co/spaces/{username}/ai-karaoke-studio
```

---

## 📦 What's Deployment-Ready

✅ **Dockerfile**
- Multi-stage build optimized for size
- Port: 7860 (HF Spaces compatible)
- Workers: 2 (HF resources)
- Security: Non-root user
- Health checks included

✅ **Environment Variables**
- `.env.example` with all required vars
- HF Spaces compatible (uses secrets)
- Production-safe defaults

✅ **Application**
- Flask production config
- SQLite database included
- Auto-cleanup (7 days)
- Error handling in place

✅ **Documentation**
- `HF_SPACES_DEPLOYMENT.md` (50+ steps)
- `HF_SPACES_CHECKLIST.md` (verification)
- `.env.example` (all variables)

---

## 🔧 Configuration Files Location

| File | Purpose |
|------|---------|
| `Dockerfile` | Container config (port 7860, 2 workers) |
| `.env.example` | Environment variables template |
| `.dockerignore` | Docker build exclusions |
| `config.py` | Flask configuration |
| `app.py` | Main application |
| `HF_SPACES_DEPLOYMENT.md` | Full guide (70+ sections) |
| `HF_SPACES_CHECKLIST.md` | Verification checklist |

---

## ⚡ Key Changes for HF Spaces

1. **Port**: 5000 → 7860
2. **Workers**: 4 → 2
3. **Threads**: 4 → 2
4. **Storage**: Ephemeral (50GB, auto-cleanup)
5. **No GPU**: Default (can upgrade)

---

## ✅ Pre-Deployment Verification

```bash
# Check Dockerfile
grep "EXPOSE 7860" Dockerfile          # ✅ Should show 7860
grep "0.0.0.0:7860" Dockerfile        # ✅ Should show 7860

# Check requirements
pip install -r requirements.txt --dry-run  # ✅ No errors

# Check Python syntax
python -m py_compile app.py           # ✅ No errors

# Check env example
cat .env.example | grep FLASK_ENV     # ✅ Should show settings
```

---

## 🚀 Deployment Steps Checklist

- [ ] **Step 1**: Create HF account (2 min)
- [ ] **Step 2**: Get API token (1 min)
- [ ] **Step 3**: Create Space (2 min)
- [ ] **Step 4**: Push code (3 min)
- [ ] **Step 5**: Set env variables (2 min)
- [ ] **Step 6**: Wait for build (5 min)
- [ ] **Step 7**: Test app (5 min)
- [ ] **Step 8**: Share link (1 min)

**Total**: ~20 minutes

---

## 📊 Port Configuration Summary

| Scenario | Port | File |
|----------|------|------|
| Local dev | 5000 | Flask default |
| Docker (HF) | 7860 | Dockerfile |
| Health check | 7860 | Dockerfile HEALTHCHECK |
| Gunicorn | 7860 | Dockerfile CMD |

✅ All configured correctly!

---

## 🔑 Required Secrets (HF Spaces)

```
FLASK_ENV=production
SECRET_KEY=<generate-32-chars>
TORCH_NUM_THREADS=2
DEMUCS_MODEL=htdemucs
ENABLE_YOUTUBE_DOWNLOAD=true
```

**Generate SECRET_KEY**:
```bash
python3 -c "import secrets; print(secrets.token_hex(16))"
```

---

## 📚 Documentation Files

1. **HF_SPACES_DEPLOYMENT.md** (MAIN GUIDE)
   - 70+ detailed sections
   - Step-by-step instructions
   - Troubleshooting guide
   - Advanced configuration

2. **HF_SPACES_CHECKLIST.md**
   - Pre-deployment checklist
   - Testing verification
   - Deployment status tracker

3. **.env.example**
   - All environment variables
   - HF Spaces notes
   - Generation instructions

4. **This file (DEPLOYMENT_QUICK_REFERENCE.md)**
   - Quick reference card
   - 5-minute summary
   - Key changes listed

---

## ⚠️ Common Mistakes to Avoid

❌ Don't: Use port 5000 in Dockerfile
✅ Do: Use port 7860

❌ Don't: Forget SECRET_KEY in production
✅ Do: Generate 32-char random key

❌ Don't: Use 4 workers on HF Spaces
✅ Do: Use 2 workers (shared resources)

❌ Don't: Commit .env file
✅ Do: Use HF Spaces Repository secrets

❌ Don't: Forget to set FLASK_ENV=production
✅ Do: Always set FLASK_ENV to production

---

## 🎯 Success Criteria

After deployment, verify:

✅ App loads (homepage visible)
✅ Upload works (can select audio)
✅ Stem separation processes (shows progress)
✅ Results display (stems visible)
✅ Model caches (2nd upload faster)
✅ No errors in logs
✅ Response time acceptable

---

## 📱 Share Your Portfolio

**Link Format**:
```
https://huggingface.co/spaces/{your-hf-username}/ai-karaoke-studio
```

**Portfolio Description**:
```
"AI Karaoke Music Studio: Real-time stem separation using 
Demucs, vocal recording, and AI performance scoring. 
Built with Flask, PyTorch, Librosa. 
Deployed on Hugging Face Spaces with GPU acceleration."
```

---

## 🆘 Quick Troubleshooting

| Problem | Fix |
|---------|-----|
| Build fails | Check Logs → Add missing dependency → Retry |
| Port error | Verify Dockerfile has 7860 (not 5000) |
| Timeout | First upload takes 30-60s (normal) |
| Storage full | 7-day auto-cleanup active (normal) |
| App won't start | Restart Space (Settings → Restart) |

See `HF_SPACES_DEPLOYMENT.md` for detailed troubleshooting.

---

## 📞 Support Resources

- **HF Spaces Docs**: https://huggingface.co/docs/hub/spaces
- **Demucs Repo**: https://github.com/facebookresearch/demucs
- **Flask Docs**: https://flask.palletsprojects.com/
- **PyTorch Docs**: https://pytorch.org/

---

## ✅ Status: DEPLOYMENT READY

All files configured ✅
All documentation complete ✅
No manual edits needed ✅

**Ready to deploy to HF Spaces!** 🚀

Start with: `HF_SPACES_DEPLOYMENT.md` → Follow **Step 1**
