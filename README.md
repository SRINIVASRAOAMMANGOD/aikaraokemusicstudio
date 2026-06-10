---
title: AI Karaoke Studio
emoji: 🎤
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# 🎵 AI-Powered STEM Karaoke Studio

A comprehensive web-based AI music processing platform that performs automatic audio stem separation, provides interactive karaoke features, real-time vocal recording, and AI-powered performance analysis.

Built with **Flask**, **PyTorch**, **Demucs**, and deployed on **Hugging Face Spaces**.

**Python 3.11 Required**

Also refer : [ai-stem-karaoke-studio]([https://huggingface.co/spaces](https://github.com/SRINIVASRAOAMMANGOD/ai-stem-karaoke-studio)) 

---

## 🚀 Project Overview

This project implements a deep learning-based music source separation system using the **Demucs** pre-trained model with advanced karaoke features.

Users can:

- Upload audio files or provide audio URLs (YouTube, direct links)
- Automatically separate music into individual stems:
  - Vocals
  - Drums
  - Bass
  - Other instruments
- Control volume, pan, solo, and mute for each stem
- Adjust master controls: tempo, pitch, volume
- Enable karaoke mode with lyrics display
- Record vocals with microphone
- Compare original vocals with recorded performance
- Get AI-powered vocal analysis and scoring
- Manage multiple projects
- Customize audio processing settings

---

## 🎯 Features

### Audio Processing
- Multiple Demucs models (htdemucs, htdemucs_ft, htdemucs_6s, mdx_extra)
- High-quality stem separation
- Real-time playback controls
- Waveform visualization

### Karaoke Features
- Interactive lyrics display
- Vocal enhancement effects (reverb, echo, auto-tune)
- Karaoke presets (Classic, Concert Hall, Studio)
- Countdown and metronome support

### Recording & Analysis
- Multi-track recording with microphone
- A/B comparison with original vocals
- AI performance scoring
- Pitch accuracy analysis
- Timing analysis
- Tone quality assessment
- Progress tracking over time

### Project Management
- Save and organize projects
- Search and filter capabilities
- Grid and list view options
- Favorite projects
- Project metadata storage

---

## ⚡ Quick Start (HF Spaces)

This app is **live and ready to use!** No installation needed.

Live site: https://srinivashugfacinging-ai-karaoke-studio.hf.space/

### How to Use

1. **Upload Audio**
   - Click "Upload Audio" and select an MP3, WAV, FLAC, OGG, M4A, or AAC file
   - Or paste a YouTube URL/direct audio link
   - Max file size: 50MB

2. **Wait for Stem Separation**
   - First upload: ~30-60 seconds (downloads AI model)
   - Subsequent uploads: ~30-40 seconds (model cached)

3. **Mix Stems**
   - Use sliders to adjust volume for each stem
   - Pan, solo, or mute individual tracks

4. **Record Karaoke** (optional)
   - Click "Record" to sing along
   - Play backing track
   - Record your vocals

5. **Get AI Score** (optional)
   - Compare your recording with original
   - Get pitch, timing, tone analysis
   - Track improvement over time

---

## 🚀 Deployment

**Status**: ✅ **Live on Hugging Face Spaces**

Live site: https://srinivashugfacinging-ai-karaoke-studio.hf.space/

This app is deployed on [Hugging Face Spaces](https://huggingface.co/spaces/WEBSITEMAN/ai-karaoke-studio) with:
- Free hosting (no credit card needed)
- Automatic scaling
- GPU acceleration available
- Always-on availability

For deployment instructions, see: [`HF_SPACES_DEPLOYMENT.md`](./HF_SPACES_DEPLOYMENT.md)

---

## � Storage Architecture

### Ephemeral Storage Design (One-Time Use Pattern)

This application is designed as a **stateless, one-time use** web service. Here's why uploaded files and project folders are not visible in Hugging Face Spaces:

#### **By Design: Session-Based Processing**
- **Uploads folder** and **projects folder** are created **dynamically at runtime** in memory/temporary storage
- Files are **not persisted** between sessions by default
- When a space restarts or session ends, temporary files are automatically cleaned up
- This is intentional for a **karaoke practice/recording tool** where users don't need long-term storage

#### **Why This Approach?**
1. **Storage Efficiency**: No accumulation of old audio files
2. **Privacy**: User recordings/uploaded music are not permanently stored
3. **One-Time Use**: Users upload → process → download/use → done
4. **Zero Maintenance**: Automatic cleanup, no manual file management needed
5. **Cost Optimization**: Minimizes HF Spaces storage quota usage (stays at 0MB)

#### **How It Works**
- User uploads audio → saved to temporary `uploads/` folder
- App processes with Demucs → saves stems to `projects/{project_id}/stems/`
- User downloads/uses files in browser session
- On next space restart → all temporary files are cleared
- Fresh space for next user

#### **If Persistent Storage Were Needed**
To make files persist in HF Spaces (for multi-session use cases), we would:
```python
# Use HF Spaces persistent storage
UPLOAD_FOLDER = '/data/uploads'
PROJECTS_FOLDER = '/data/projects'
```
This would require:
- Storage quota on HF Spaces
- Auto-cleanup policies to manage disk space
- Database indexing for file retrieval
- Not needed for current one-time use design

#### **Key Insight for Interviews**
✅ This is a **design choice**, not a limitation:
- Prioritizes user privacy and clean resource usage
- Optimized for stateless cloud deployment (HF Spaces, Docker, Kubernetes)
- Typical pattern for ML inference services and batch processing tools
- Can be modified to use persistent storage if requirements change

---

## �🔧 Installation (Local Development)

```
User Interface (Flask Templates)
├── Base Layout (base.html)
├── Home Page (home.html)
└── Components
    ├── Navigation
    ├── Upload Section (File/URL)
    ├── Progress Bar
    ├── Waveform Visualization
    ├── Stem Controls (4 channels)
    ├── Master Controls
    ├── Karaoke Mode
    ├── Recording Studio
    ├── A/B Comparison
    ├── AI Score Dashboard
    ├── Projects Manager
    └── Settings Panel

Backend API (Flask)
├── Upload Endpoints
├── Stem Separation Service (Demucs)
├── URL Download Service (yt-dlp)
├── Recording Management
├── AI Analysis Engine
├── Project Database (SQLite)
└── Settings Storage
```

---

## 🛠️ Tech Stack

- **Backend:** Flask 3.0+
- **AI Model:** Demucs 4.0+ (Hybrid Transformer)
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Audio Visualization:** WaveSurfer.js
- **Database:** SQLite 3
- **Audio Processing:** PyTorch, FFmpeg
- **URL Processing:** yt-dlp
- **Icons:** Font Awesome 6+

---

## 📂 Project Structure

```
ai-stem-karaoke-studio/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
│
├── database/
│   ├── __init__.py
│   └── db.py                   # Database operations
│
├── services/
│   ├── __init__.py
│   ├── demucs_service.py       # Stem separation
│   └── url_service.py          # URL download handling
│
├── templates/
│   ├── base.html               # Base template
│   ├── home.html               # Main page
│   ├── index.html              # Original index (legacy)
│   ├── result.html             # Original result (legacy)
│   └── components/
│       ├── navbar.html
│       ├── upload_section.html
│       ├── progress_bar.html
│       ├── waveform_section.html
│       ├── stem_controls.html
│       ├── master_controls.html
│       ├── karaoke_controls.html
│       ├── recording_controls.html
│       ├── comparison_layout.html
│       ├── ai_score_dashboard.html
│       ├── projects_list.html
│       └── settings_panel.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── uploads/                    # Uploaded audio files
├── separated/                  # Separated stems output
└── karaoke_studio.db          # SQLite database
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd ai-stem-karaoke-studio
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Initialize Database

```bash
python -c "from database.db import init_db; init_db()"
```

### 5️⃣ Run Application

```bash
python app.py
```

### 6️⃣ Access Application

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🚀 Production Deployment

### Docker Deployment (Recommended)

For production environments, use Docker with the provided production-ready Dockerfile:

```bash
# Build image
docker build -t aikaraoke:latest .

# Generate secure SECRET_KEY
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# Run with Docker Compose
docker-compose up -d
```

### Access Points

- **Application**: http://yourdomain.com (HTTPS recommended)
- **Health Check**: http://yourdomain.com/health
- **API**: http://yourdomain.com/api/*

### Production Features

✅ **Security**
- Non-root user execution
- SSL/TLS support with Nginx
- Environment variable configuration
- Secret key validation

✅ **Performance**
- Multi-stage Docker build
- Optimized gunicorn configuration
- Health check monitoring
- Resource limits

✅ **Operations**
- Automatic container restart
- Persistent volume management
- Structured logging
- Docker Compose orchestration

### Deployment Documentation

See detailed deployment guides:
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Comprehensive production deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment checklist
- **[docker-compose.yml](docker-compose.yml)** - Production Docker Compose configuration
- **[nginx.conf](nginx.conf)** - Nginx reverse proxy configuration
- **[.env.example](.env.example)** - Environment variables template

### Quick Production Deploy

```bash
# 1. Clone repository
git clone <your-repo> aikaraoke
cd aikaraoke

# 2. Set up environment
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
cp .env.example .env
# Edit .env with your configuration

# 3. Create data directories
mkdir -p uploads projects logs

# 4. Deploy
docker-compose up -d

# 5. Verify health
curl http://localhost:5000/health
```

### SSL/HTTPS Setup

```bash
# Using Let's Encrypt + Certbot
mkdir -p ssl
certbot certonly --standalone -d yourdomain.com

# Copy certificates
cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem

# Restart services with Nginx
docker-compose down
docker-compose up -d
```

### Monitoring

```bash
# View logs
docker-compose logs -f web

# Check health
docker-compose exec web curl http://localhost:5000/health

# Monitor resources
docker stats aikaraoke-studio
```

### Backup Strategy

```bash
# Backup projects
tar -czf backup-$(date +%Y%m%d).tar.gz projects/

# Automated daily backup (cron)
0 2 * * * tar -czf /backups/aikaraoke-$(date +\%Y\%m\%d).tar.gz /path/to/projects/
```

For comprehensive deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🎮 Usage Guide

### Upload Audio
1. Navigate to the home page
2. Choose between "Upload File" or "From URL"
3. Select audio file or paste URL (YouTube supported)
4. Choose Demucs model
5. Click "Separate Stems"

### Control Stems
- Use volume sliders for each stem
- Pan controls for stereo positioning
- Solo/Mute buttons for individual stems
- Download individual stems

### Karaoke Mode
1. Toggle karaoke mode ON
2. Add or import lyrics
3. Adjust vocal enhancements
4. Choose preset or customize settings

### Record Performance
1. Select microphone from device list
2. Adjust input gain
3. Enable count-in if desired
4. Click "Record" to start
5. Save or discard takes

### AI Analysis
1. Record your vocal performance
2. Click "Analyze Performance"
3. View detailed metrics and scores
4. Get personalized feedback
5. Track progress over time

---

## 🔧 API Endpoints

### Audio Processing
- `POST /upload` - Upload and process audio file
- `POST /upload-url` - Download and process from URL
- `GET /separated/<path>` - Serve separated audio files

### Project Management
- `GET /api/projects` - Get all projects
- `GET /api/projects/<id>` - Get specific project
- `DELETE /api/projects/<id>` - Delete project
- `POST /api/projects/<id>/favorite` - Toggle favorite

### Recording
- `POST /api/save-recording` - Save vocal recording
- `POST /api/analyze-performance` - AI analysis

### Settings
- `GET /api/settings` - Get settings
- `POST /api/settings` - Save settings

### Utilities
- `GET /api/models` - Get available models
- `GET /api/check-demucs` - Check Demucs installation

---

## 🎛️ Configuration

Edit `config.py` to customize:
- Upload folder paths
- Max file size
- Allowed file formats
- Default Demucs model
- Session settings
- Feature flags

---

## 📋 Requirements

### System Requirements
- Python 3.11.x
- 4GB+ RAM recommended
- GPU optional (for faster processing)

### Python Packages
See `requirements.txt` for full list:
- Flask 3.0+
- PyTorch 2.2+
- Demucs 4.0+
- yt-dlp (for YouTube support)
- requests
- werkzeug

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secure-32-character-random-key

# AI Model
DEMUCS_MODEL=htdemucs
TORCH_NUM_THREADS=4

# Storage
UPLOAD_FOLDER=uploads
DATABASE_FILE=karaoke_studio.db

# Features
ENABLE_YOUTUBE_DOWNLOAD=true
ENABLE_AI_ANALYSIS=true

# Logging
LOG_LEVEL=info
```

**For HF Spaces**: Use "Repository secrets" in Space settings instead of .env file.

See [.env.example](.env.example) for complete configuration options.

---

## 🐛 Troubleshooting

### Demucs Not Found
```bash
pip install demucs
```

### YouTube Download Issues
```bash
pip install --upgrade yt-dlp
```

### Database Errors
```bash
# Reinitialize database
python -c "from database.db import init_db; init_db()"
```

---

## 📝 License

[Your License Here]

---

## 📚 Documentation

- **[START_HERE.md](START_HERE.md)** - Quick start guide for deployment
- **[HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md)** - Complete HF Spaces deployment guide (70+ sections)
- **[HF_SPACES_CHECKLIST.md](HF_SPACES_CHECKLIST.md)** - Deployment verification checklist
- **[DEPLOYMENT_QUICK_REFERENCE.md](DEPLOYMENT_QUICK_REFERENCE.md)** - Quick reference card
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - General production deployment guide
- **[.env.example](.env.example)** - Environment variables template

---

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/WEBSITEMAN/ai-karaoke-studio/issues)
- **HF Spaces**: [Live Demo](https://huggingface.co/spaces/WEBSITEMAN/ai-karaoke-studio)
- **Documentation**: See deployment guides above

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 🎓 Credits

- **Demucs**: [Meta AI](https://github.com/facebookresearch/demucs)
- **Flask**: [Pallets](https://flask.palletsprojects.com/)
- **PyTorch**: [Meta AI](https://pytorch.org/)
- **Librosa**: [Brain](https://librosa.org/)
- **Hosting**: [Hugging Face Spaces](https://huggingface.co/spaces)

---

**Status**: ✅ **Live and Ready**
**Platform**: Hugging Face Spaces
**Last Updated**: 2026-05-25


---

## 🙏 Acknowledgments

- Demucs by Meta AI Research
- Flask framework
- WaveSurfer.js
- Font Awesome icons
