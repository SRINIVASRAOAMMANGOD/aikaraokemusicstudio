# 🚀 Deployment Guide - Railway.app (FREE)

## Quick Start (5 minutes)

### Step 1: Prepare Your Repository
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for deployment"
```

### Step 2: Push to GitHub
1. Create a new repository on GitHub (https://github.com/new)
2. Name it something like `ai-karaoke-studio`
3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/ai-karaoke-studio.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on Railway
1. Go to **https://railway.app**
2. Sign up (use GitHub for easiest login)
3. Click **"Create a new project"** → **"Deploy from GitHub"**
4. Select your `ai-karaoke-studio` repository
5. Railway will auto-detect Python and deploy!

### Step 4: Set Environment Variables
In Railway dashboard:
1. Go to your project → **Variables** tab
2. Add these:
```
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
```
3. Click **"Deploy"** to rebuild

---

## ⚠️ Important: Storage Limitations

Railway free tier has **ephemeral storage** (resets on redeploy). For your app:

### ❌ Problem
- `uploads/` folder gets deleted on redeploy
- `projects/` folder gets deleted
- Database (`karaoke_studio.db`) gets deleted

### ✅ Solution Options

#### Option A: Use S3 (Recommended for scalability)
Add AWS S3 for file storage (free tier available):
```python
# In your app, replace:
# uploads/ → S3 bucket
# projects/ → S3 bucket
```

#### Option B: Accept Temporary Storage (Simple)
- Users can upload files, process them, download results in the same session
- Data is lost on app restart (acceptable for personal use)
- No changes needed to your code

---

## 🎯 Performance Tips

### Model Caching (Critical!)
The Demucs model (~400MB) downloads on first use. To avoid timeout:

1. **Pre-warm the model** - Create a startup hook in your app:
```python
# Add to app.py before running
import threading
def load_demucs_model():
    """Pre-load Demucs model on startup"""
    try:
        from services.demucs_service import separate_audio
        # This triggers model download
        print("✓ Demucs model pre-loaded")
    except Exception as e:
        print(f"Note: Model will load on first processing request: {e}")

# Run in background thread
thread = threading.Thread(target=load_demucs_model, daemon=True)
thread.start()
```

2. **Increase timeout** - Already set to 120s in Procfile

### CPU Processing
- Light usage (1-2 files/day) = Free tier sufficient
- Busy usage = Upgrade to paid plan ($7/month)

---

## 📊 Free Tier Limits

| Resource | Free | Limit |
|----------|------|-------|
| **Compute** | Always on | 500 CPU hours/month |
| **Memory** | 512MB - 8GB | Shared |
| **Storage** | Ephemeral | Resets on deploy |
| **Bandwidth** | ✓ Unlimited | - |
| **Credit** | $5/month | Expires monthly |

**Your usage**: ~10-15 CPU hours/month (well within free limit)

---

## 🔐 Security Checklist

- [ ] Set `FLASK_ENV=production` on Railway
- [ ] Generate strong `SECRET_KEY` (use Python: `import secrets; print(secrets.token_hex(32))`)
- [ ] Don't commit secrets to GitHub
- [ ] Update `SESSION_COOKIE_SECURE=True` once you have HTTPS (Railway provides free SSL)

---

## 🐛 Troubleshooting

### App won't start
- Check Railway logs: Project → Logs tab
- Common issue: Missing `SECRET_KEY` environment variable

### Audio processing timeout
- Processing takes 30-60s per file on free tier
- Increase Procfile timeout: `--timeout 180`

### File deleted after restart
- This is expected! Use Option A (S3) if you need persistence

### Out of storage
- Clean up old `uploads/projects` on Railway dashboard file browser

---

## 📈 Next Steps (After Deployment)

### Phase 1: Monitor
- Watch Railway dashboard for CPU/memory usage
- Check app logs for errors

### Phase 2: Optimize (if needed)
- Enable GPU acceleration (requires paid plan)
- Switch to lighter Demucs model (`mdx_extra_q`)
- Implement file cleanup strategy

### Phase 3: Scale (when popular)
- Upgrade Railway plan (+$7/month)
- Add cloud storage (Google Drive / AWS S3)
- Distribute audio processing using task queue

---

## 🎵 Your App URL

After deployment, your app will be at:
```
https://ai-karaoke-studio-XXX.railway.app
```

Share this link with friends!

---

## 💰 Cost Breakdown

| Month 1+ | Cost |
|----------|------|
| Railway compute | $0 (within free $5 credit) |
| Storage (optional S3) | $0-$1/month |
| Custom domain | $0 (optional) |
| **Total** | **FREE** 🎉 |

---

**Questions?** Check Railway docs: https://docs.railway.app
