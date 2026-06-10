# Production Changes & Updates Guide

Complete guide to set up your repository for making changes and pushing updates to production (GitHub and Hugging Face Spaces).

---

## 📋 Table of Contents

1. [Initial Setup](#initial-setup)
2. [Add GitHub Remote](#add-github-remote)
3. [Add Hugging Face Remote](#add-hugging-face-remote)
4. [Making Changes & Pushing Updates](#making-changes--pushing-updates)
5. [Workflow Examples](#workflow-examples)
6. [Troubleshooting](#troubleshooting)

---

## Initial Setup

### Step 1: Create a New Folder for Your Project

**On Windows (PowerShell):**
```powershell
# Create main project folder
mkdir C:\Users\HP\Desktop\deployment\ai-karaoke-studio
cd C:\Users\HP\Desktop\deployment\ai-karaoke-studio

# Initialize Git repository
git init

# Configure Git (use your GitHub username and email)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Create main branch
git branch -m main

# Verify setup
git status
```

**On Mac/Linux:**
```bash
mkdir ~/ai-karaoke-studio
cd ~/ai-karaoke-studio

git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git branch -m main

git status
```

### Step 2: Add Project Files

Copy or add your project files to the folder:
- `app.py`
- `config.py`
- `requirements.txt`
- `Dockerfile`
- `docker-compose.yml`
- `static/`, `templates/`, `services/`, `database/` folders
- `.env.example`
- `.gitignore`
- `README.md`

---

## Add GitHub Remote

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click **New Repository** (top-right)
3. Set repository name: `ai-karaoke-studio`
4. Add description: "AI-Powered Music Stem Karaoke Studio"
5. Choose **Public** or **Private**
6. Click **Create Repository**
7. **Copy the HTTPS URL** (e.g., `https://github.com/YOUR-USERNAME/ai-karaoke-studio.git`)

### Step 2: Add GitHub as Remote

```bash
# Navigate to your project folder
cd C:\Users\HP\Desktop\deployment\ai-karaoke-studio

# Add GitHub remote (replace USERNAME with your GitHub username)
git remote add github https://github.com/YOUR-USERNAME/ai-karaoke-studio.git

# Verify remote was added
git remote -v
```

**Expected output:**
```
github  https://github.com/YOUR-USERNAME/ai-karaoke-studio.git (fetch)
github  https://github.com/YOUR-USERNAME/ai-karaoke-studio.git (push)
```

### Step 3: Push to GitHub

```bash
# Stage all files
git add .

# Commit initial changes
git commit -m "Initial commit: AI Karaoke Studio project setup"

# Push to GitHub main branch
git push github main
```

**First time push troubleshooting:**
- You may be prompted for authentication
- Use a **GitHub Personal Access Token** (not your password)
- Generate token at: https://github.com/settings/tokens
- Scope needed: `repo` (full control of private repositories)

---

## Add Hugging Face Remote

### Step 1: Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **Create new Space**
3. Set **Space name**: `ai-karaoke-studio`
4. Choose **SDK**: `Docker`
5. Set **Docker build context**: `/` (default)
6. Set **Docker main file location**: `Dockerfile` (default)
7. Space visibility: **Public** or **Private**
8. Click **Create Space**
9. **Copy the Git clone URL** (e.g., `https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio.git`)

### Step 2: Add Hugging Face as Remote

```bash
# From your project folder
cd C:\Users\HP\Desktop\deployment\ai-karaoke-studio

# Add HF as remote (replace USERNAME with your HF username)
git remote add huggingface https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio.git

# Verify remotes
git remote -v
```

**Expected output:**
```
github          https://github.com/YOUR-USERNAME/ai-karaoke-studio.git (fetch)
github          https://github.com/YOUR-USERNAME/ai-karaoke-studio.git (push)
huggingface     https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio.git (fetch)
huggingface     https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio.git (push)
```

### Step 3: Set HF API Token

For authentication without entering credentials:

```bash
# Generate HF API token at https://huggingface.co/settings/tokens
# Store as environment variable (Windows PowerShell)
$env:HF_TOKEN = "your_huggingface_api_token"

# Or for permanent setup, add to PowerShell profile
# Add this to $PROFILE file:
$env:HF_TOKEN = "your_huggingface_api_token"
```

### Step 4: Push to Hugging Face

```bash
# Push to Hugging Face Space
git push huggingface main
```

---

## Making Changes & Pushing Updates

### Workflow for Daily Development

```bash
# 1. Check status
git status

# 2. Make changes to your files
# (Edit app.py, config.py, templates, etc.)

# 3. Stage changes
git add .
# OR stage specific files
git add app.py config.py

# 4. Commit with meaningful message
git commit -m "Feature: Add new karaoke controls"

# 5. Push to both GitHub and Hugging Face
git push github main
git push huggingface main
```

### Example: Making and Deploying a Change

**Scenario:** You want to update the karaoke controls feature.

```bash
# 1. Create a feature branch (optional but recommended)
git checkout -b feature/improved-karaoke-controls

# 2. Make your changes
# Edit: templates/karaoke.html
# Edit: static/js/script.js
# Edit: app.py

# 3. Test locally
python app.py  # Test on http://localhost:5000

# 4. Stage and commit
git add templates/karaoke.html static/js/script.js app.py
git commit -m "Improve karaoke control UI and responsiveness"

# 5. Merge back to main
git checkout main
git merge feature/improved-karaoke-controls

# 6. Push to both remotes
git push github main
git push huggingface main

# Watch deployment on HF: https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio
```

---

## Workflow Examples

### Example 1: Quick Bug Fix

```bash
# Make a quick fix
git add app.py
git commit -m "Fix: Correct audio upload validation error"
git push github main && git push huggingface main
```

### Example 2: Multiple Features at Once

```bash
# Create feature branch
git checkout -b feature/stem-visualization

# Make multiple changes
git add static/js/visualization.js templates/mixer.html services/demucs_service.py
git commit -m "Add stem waveform visualization with real-time updates"

# Merge and push
git checkout main
git merge feature/stem-visualization
git push github main && git push huggingface main
```

### Example 3: Update Dependencies

```bash
# Update requirements.txt with new packages
# Edit: requirements.txt

git add requirements.txt
git commit -m "Update dependencies: Add librosa==0.10.0"
git push github main && git push huggingface main

# HF will rebuild Docker image with new dependencies
```

### Example 4: Environment Configuration Changes

```bash
# Update environment settings
# Edit: .env.example
# Edit: config.py

git add .env.example config.py
git commit -m "Config: Add new audio processing settings"
git push github main && git push huggingface main
```

---

## Helpful Commands

### Check Remote Status
```bash
# See all remotes
git remote -v

# See details of a remote
git remote show github
git remote show huggingface
```

### Pull Latest Changes
```bash
# Pull from GitHub
git pull github main

# Pull from Hugging Face
git pull huggingface main
```

### View Commit History
```bash
# See last 10 commits
git log --oneline -10

# See commits with files changed
git log --name-status --oneline -5
```

### Create Branches for Organization
```bash
# Create feature branch
git checkout -b feature/new-feature-name

# Create bugfix branch
git checkout -b bugfix/issue-description

# Create release branch
git checkout -b release/v1.0.0

# List all branches
git branch -a
```

### Undo Changes
```bash
# Undo uncommitted changes to a file
git restore filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## Hugging Face Deployment

### Monitor Space Deployment

1. Go to your Space: https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio
2. Click **Logs** tab to see build progress
3. Wait for:
   - ✅ "Building container..." → Complete
   - ✅ "Launching space..." → Ready
   - **Takes 3-10 minutes depending on dependencies**

### Check Deployment Status
```bash
# From command line - check if space is running
curl https://huggingface.co/spaces/YOUR-USERNAME/ai-karaoke-studio
```

### Handle Failed Deployments
- Check **Logs** tab in HF Space
- Common issues:
  - Missing dependencies → Update `requirements.txt`
  - Port mismatch → Should be `7860` for HF
  - Memory issues → Reduce model size or optimize code
- Fix locally → Commit → Push again

---

## Best Practices

### ✅ DO

- ✅ Write clear commit messages
- ✅ Test changes locally before pushing
- ✅ Use feature branches for major changes
- ✅ Push to both GitHub and HF together
- ✅ Monitor HF logs after each deployment
- ✅ Keep `.gitignore` updated with uploads, projects, cache folders
- ✅ Document your changes in commit messages

### ❌ DON'T

- ❌ Commit large audio files (use `.gitignore`)
- ❌ Commit credentials or API keys (use `.env.example`)
- ❌ Push directly to main without testing
- ❌ Push to one remote and forget the other
- ❌ Commit generated files (cache, logs, temp files)

---

## Troubleshooting

### Push Fails with "Authentication Failed"

**Solution:**
```bash
# Generate GitHub Personal Access Token
# https://github.com/settings/tokens
# Scopes: repo (full control of private repositories)

# Then push again - you'll be prompted for token
git push github main
```

### Remote Already Exists Error

```bash
# If you get "fatal: remote github already exists"
git remote remove github
git remote add github https://github.com/YOUR-USERNAME/ai-karaoke-studio.git
```

### Branches Out of Sync

```bash
# Fetch latest from both remotes
git fetch github
git fetch huggingface

# Check what changed
git log github/main..huggingface/main

# Merge if needed
git merge huggingface/main
```

### Large Files Causing Issues

```bash
# Check file sizes
git ls-files -z | xargs -0 du -Sh | sort -rhS | head -20

# Add to .gitignore
echo "*.mp3" >> .gitignore
echo "*.wav" >> .gitignore
echo "uploads/" >> .gitignore
```

### HF Space Stuck Building

1. Go to Space settings
2. Click **Restart** button
3. Check logs for error messages
4. If still failing, push a fix and rebuild

---

## Quick Reference Cheatsheet

```bash
# Initial setup
git init
git remote add github https://github.com/USERNAME/ai-karaoke-studio.git
git remote add huggingface https://huggingface.co/spaces/USERNAME/ai-karaoke-studio.git

# Daily workflow
git add .
git commit -m "Description of changes"
git push github main && git push huggingface main

# Check status
git status
git remote -v
git log --oneline -5
```

---

## Next Steps

1. ✅ Create GitHub repository
2. ✅ Create Hugging Face Space
3. ✅ Add both remotes
4. ✅ Make initial push
5. ✅ Monitor HF deployment (check Logs)
6. ✅ Test deployed application
7. ✅ Start making updates!

For issues with specific features, check:
- [HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md) - Detailed HF setup
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Deployment verification
- [README.md](README.md) - Project features and overview

