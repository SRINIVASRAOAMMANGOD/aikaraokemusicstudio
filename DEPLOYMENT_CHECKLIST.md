# ✅ Pre-Deployment Checklist

## Files Created/Ready ✓
- [x] `Procfile` - Tells Railway how to run your app
- [x] `requirements.txt` - Has Flask, Gunicorn, Demucs, PyTorch
- [x] `config.py` - Production config ready
- [x] `app.py` - Uses FLASK_ENV for environment detection

## Before Pushing to GitHub

### Step 1: Review your code
```bash
# Make sure everything works locally first
python app.py
# Visit http://localhost:5000
```

### Step 2: Create `.gitignore` additions
Add these to your `.gitignore`:
```
# Don't commit these
.env
*.db
uploads/*
projects/*
venv/
__pycache__/
```

### Step 3: Initialize Git (if needed)
```bash
git init
git add .
git commit -m "Prepare for deployment"
```

---

## Railway Deployment Checklist

1. **Create GitHub Account**
   - Go to https://github.com/join
   - Choose your username

2. **Create Repository**
   - https://github.com/new
   - Name: `ai-karaoke-studio`
   - Public or Private

3. **Push Code**
   ```bash
   git remote add origin https://github.com/USERNAME/ai-karaoke-studio.git
   git branch -M main
   git push -u origin main
   ```

4. **Create Railway Account**
   - https://railway.app
   - Sign up → "Continue with GitHub"

5. **Connect to GitHub**
   - Click "Create Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway
   - Select your `ai-karaoke-studio` repo

6. **Set Environment Variables** (CRITICAL!)
   - In Railway, go to your project
   - Click "Variables" tab
   - Add:
     ```
     FLASK_ENV=production
     SECRET_KEY=(generate: python -c "import secrets; print(secrets.token_hex(32))")
     ```
   - Save → Redeploy

7. **Wait for Deployment**
   - Takes ~2-3 minutes
   - Check "Deployments" tab for status

8. **Get Your URL**
   - Click "Generate Domain"
   - Your app is now live! 🎉

---

## Testing Production
```bash
curl https://your-app-name.railway.app/
```

Should return status 200 with your homepage HTML.

---

## Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| Deployment stuck | Check Railway logs, look for errors |
| 502 Bad Gateway | Usually `SECRET_KEY` missing - add it to Variables |
| Model timeout | Already fixed in Procfile (120s timeout) |
| Files disappear | Normal - Railway free tier is ephemeral |

---

## Next: Monitor Your App
- Railway dashboard shows real-time stats
- Free tier supports ~100 simultaneous users
- Your usage will likely be <1 CPU hour/month

**You're ready to deploy!** 🚀
