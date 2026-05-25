# Production Deployment Guide

## Overview

This document provides comprehensive instructions for deploying the AI Karaoke Music Studio in production environments.

## Prerequisites

- Docker & Docker Compose installed
- Minimum 2 CPU cores, 4GB RAM (8GB+ recommended for better performance)
- 20GB+ storage for audio processing and project files
- Linux host (AWS EC2, DigitalOcean, Linode, Azure VM, etc.)

## Docker Image

The Dockerfile uses a **multi-stage build** for optimal production images:

- **Stage 1 (Builder)**: Compiles Python wheels with all dependencies
- **Stage 2 (Runtime)**: Lightweight image with only runtime dependencies

### Build Image

```bash
docker build -t aikaraoke:latest .
```

### Image Features

✅ **Security**
- Non-root user execution (UID 1000)
- Minimal attack surface (no build tools in final image)
- Health check endpoint for auto-restart on failure

✅ **Performance**
- Multi-stage build reduces image size ~60%
- Optimized gunicorn configuration
- Efficient worker management

✅ **Observability**
- Structured logging to stdout
- Health check status
- Container orchestration compatible

## Environment Variables

Set these before running:

```bash
# Flask settings
export FLASK_ENV=production
export SECRET_KEY=your-secure-random-key-here-min-32-chars

# Optional: Customize audio settings
export DEMUCS_MODEL=htdemucs          # Model: htdemucs, htdemucs_ft, mdx_extra
export TORCH_NUM_THREADS=4             # CPU threads for PyTorch
export UPLOAD_FOLDER=/app/uploads       # Upload directory
export PROJECTS_FOLDER=/app/projects    # Projects directory

# Optional: For GPU acceleration
export CUDA_VISIBLE_DEVICES=0           # GPU device ID
```

**Important**: Generate a secure `SECRET_KEY`:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Deployment Methods

### 1. Docker Compose (Recommended)

```yaml
# docker-compose.yml
version: '3.8'

services:
  aikaraoke:
    image: aikaraoke:latest
    build: .
    container_name: aikaraoke-prod
    
    ports:
      - "5000:5000"
    
    environment:
      FLASK_ENV: production
      SECRET_KEY: ${SECRET_KEY}
      DEMUCS_MODEL: htdemucs
    
    volumes:
      - ./uploads:/app/uploads
      - ./projects:/app/projects
      - ./logs:/app/logs
    
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    
    networks:
      - aikaraoke-net
    
    # Resource limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

  # Optional: Nginx reverse proxy
  nginx:
    image: nginx:alpine
    container_name: aikaraoke-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - aikaraoke
    networks:
      - aikaraoke-net

networks:
  aikaraoke-net:
    driver: bridge
```

Deploy:

```bash
export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
docker-compose up -d
```

### 2. Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aikaraoke
spec:
  replicas: 2
  selector:
    matchLabels:
      app: aikaraoke
  template:
    metadata:
      labels:
        app: aikaraoke
    spec:
      containers:
      - name: aikaraoke
        image: aikaraoke:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: aikaraoke-secrets
              key: secret-key
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        volumeMounts:
        - name: uploads
          mountPath: /app/uploads
        - name: projects
          mountPath: /app/projects
      volumes:
      - name: uploads
        persistentVolumeClaim:
          claimName: aikaraoke-uploads-pvc
      - name: projects
        persistentVolumeClaim:
          claimName: aikaraoke-projects-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: aikaraoke-service
spec:
  selector:
    app: aikaraoke
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

Deploy:

```bash
kubectl create secret generic aikaraoke-secrets \
  --from-literal=secret-key="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"

kubectl apply -f deployment.yaml
```

### 3. Manual Linux

```bash
# Clone repository
git clone <your-repo> aikaraoke
cd aikaraoke

# Build image
docker build -t aikaraoke:latest .

# Create persistent volumes
mkdir -p /var/aikaraoke/{uploads,projects,logs}
chmod 1000:1000 /var/aikaraoke/*

# Run container
docker run -d \
  --name aikaraoke-prod \
  --restart always \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" \
  -v /var/aikaraoke/uploads:/app/uploads \
  -v /var/aikaraoke/projects:/app/projects \
  aikaraoke:latest

# View logs
docker logs -f aikaraoke-prod
```

## Reverse Proxy Setup (Nginx)

```nginx
# /etc/nginx/sites-available/aikaraoke.conf

upstream aikaraoke {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name yourdomain.com;

    client_max_body_size 50M;  # Match FLASK MAX_CONTENT_LENGTH

    location / {
        proxy_pass http://aikaraoke;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout for long-running audio processing
        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
    }

    location /health {
        proxy_pass http://aikaraoke;
        access_log off;
    }
}

# Enable SSL with Let's Encrypt
# sudo certbot --nginx -d yourdomain.com
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/aikaraoke.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/TLS Configuration

### Using Let's Encrypt (Certbot)

```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com --non-interactive --agree-tos -m your-email@example.com
```

Auto-renewal:

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Storage Management

### Volume Mounting

```bash
# Create persistent volumes
docker volume create aikaraoke-uploads
docker volume create aikaraoke-projects

# Use in docker-compose.yml
volumes:
  uploads:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/data/uploads
  projects:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /mnt/data/projects
```

### Cleanup Strategy

The application automatically:
- Deletes projects older than 7 days
- Cleans up temporary files
- Respects storage quota settings

Manual cleanup:

```bash
# Clear cache
curl -X POST http://localhost:5000/api/clear-cache

# Remove old projects
docker exec aikaraoke-prod python3 -c "
import shutil
import os
from datetime import datetime, timedelta

projects_dir = 'projects'
cutoff = datetime.now() - timedelta(days=7)

for folder in os.listdir(projects_dir):
    path = os.path.join(projects_dir, folder)
    if os.path.isdir(path):
        mod_time = datetime.fromtimestamp(os.path.getmtime(path))
        if mod_time < cutoff:
            shutil.rmtree(path)
            print(f'Deleted {folder}')
"
```

## Monitoring & Logging

### View Logs

```bash
# Docker
docker logs -f aikaraoke-prod

# Container logs
docker logs --tail=100 aikaraoke-prod

# Kubernetes
kubectl logs -f deployment/aikaraoke
```

### Health Check

```bash
curl http://localhost:5000/health

# Output
{
  "status": "healthy",
  "service": "AI Karaoke Music Studio",
  "timestamp": "2026-05-17T10:30:45.123456"
}
```

### Performance Metrics

Monitor:
- CPU usage (FFmpeg, PyTorch intensive)
- Memory usage (PyTorch models ~2GB)
- Disk I/O (audio processing)
- API response times

```bash
# Check container stats
docker stats aikaraoke-prod

# Monitor system resources
top -p $(docker inspect -f '{{.State.Pid}}' aikaraoke-prod)
```

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs aikaraoke-prod

# Validate environment
docker exec aikaraoke-prod env | grep FLASK

# Test health endpoint
docker exec aikaraoke-prod curl http://localhost:5000/health
```

### Out of memory

Symptoms: Container restarts, OOMKilled errors

Solutions:
```bash
# Increase container memory
docker update --memory 8g aikaraoke-prod

# Reduce worker count
# Edit CMD in Dockerfile: --workers 2 (was 4)

# Enable aggressive cleanup
curl -X POST http://localhost:5000/api/clear-cache
```

### Slow audio processing

- Increase CPU cores/memory allocation
- Reduce concurrent uploads (limit connections)
- Use faster model: `DEMUCS_MODEL=htdemucs_6s`

### HTTPS issues

```bash
# Verify SSL certificate
sudo openssl x509 -in /etc/letsencrypt/live/yourdomain.com/cert.pem -text

# Force HTTPS redirect
# Add to Dockerfile CMD or Flask config
app.config['SESSION_COOKIE_SECURE'] = True
```

## Performance Tuning

### Gunicorn Workers

Formula: `(2 × CPU cores) + 1`

For 4 cores: `--workers 9` (current: 4)

Edit Dockerfile CMD section:

```dockerfile
CMD ["gunicorn", \
     "--workers", "9", \  # Increase this
     ...
     "app:app"]
```

### GPU Acceleration

For NVIDIA GPUs:

```dockerfile
FROM nvidia/cuda:12.1-runtime-ubuntu22.04

# Install PyTorch with GPU support
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Docker Compose:

```yaml
services:
  aikaraoke:
    runtime: nvidia
    environment:
      - CUDA_VISIBLE_DEVICES=0
```

## Security Checklist

- ✅ Non-root user execution
- ✅ Environment variables (no secrets in Dockerfile)
- ✅ HTTPS/SSL enabled
- ✅ Firewall rules (port 5000 internal only)
- ✅ Regular backups of projects
- ✅ File upload validation
- ✅ Rate limiting implemented
- ✅ CSRF protection enabled
- ✅ Secret key rotated

## Backup Strategy

```bash
# Backup projects
tar -czf backup-$(date +%Y%m%d).tar.gz /var/aikaraoke/projects/

# Backup to cloud (S3)
aws s3 sync /var/aikaraoke/projects/ s3://backup-bucket/aikaraoke/projects/

# Schedule daily backup
0 2 * * * tar -czf /backups/aikaraoke-$(date +\%Y\%m\%d).tar.gz /var/aikaraoke/projects/
```

## Scaling

### Horizontal Scaling (Multiple Instances)

```yaml
# docker-compose with load balancing
services:
  aikaraoke-1:
    image: aikaraoke:latest
    # ...
  
  aikaraoke-2:
    image: aikaraoke:latest
    # ...
  
  nginx:
    image: nginx:alpine
    # Load balance across instances
```

### Shared Storage

Use network storage (NFS, S3) for projects and uploads:

```bash
# NFS mount
mount -t nfs 192.168.1.100:/exports/aikaraoke /var/aikaraoke

# Or S3
pip install s3fs
# Configure in Flask config
```

## Support

For issues:
1. Check logs: `docker logs aikaraoke-prod`
2. Verify health: `curl http://localhost:5000/health`
3. Test API: `curl -X GET http://localhost:5000/api/projects`
4. Review configuration: `docker exec aikaraoke-prod env`
