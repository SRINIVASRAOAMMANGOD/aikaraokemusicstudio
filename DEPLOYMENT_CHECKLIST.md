# Production Deployment Checklist

## Pre-Deployment

- [ ] **Docker Engine & Compose**: Verify installation and versions
  ```bash
  docker --version
  docker-compose --version
  ```

- [ ] **System Requirements**: Verify host meets specs
  - [ ] Minimum 2 CPU cores (4+ recommended)
  - [ ] Minimum 4GB RAM (8GB+ recommended)
  - [ ] At least 50GB free disk space
  - [ ] Linux host (Ubuntu 20.04+ recommended)

- [ ] **Repository**: Clone and navigate to project
  ```bash
  git clone <your-repo> aikaraoke
  cd aikaraoke
  ```

- [ ] **Environment Variables**: Create configuration
  ```bash
  # Generate secure SECRET_KEY
  export SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  
  # Export other variables
  export FLASK_ENV=production
  export DEMUCS_MODEL=htdemucs
  export LOG_LEVEL=info
  ```

- [ ] **Environment File**: Copy and customize
  ```bash
  cp .env.example .env
  # Edit .env with your values
  ```

- [ ] **Directories**: Create necessary directories
  ```bash
  mkdir -p uploads projects logs
  chmod 1000:1000 uploads projects logs  # appuser UID:GID
  ```

## Docker Build & Push

- [ ] **Build Image**: Build Docker image
  ```bash
  docker build -t aikaraoke:latest .
  docker build -t yourdomain.com/aikaraoke:latest .  # For registry
  ```

- [ ] **Test Image**: Run and test locally
  ```bash
  docker run -it -p 5000:5000 \
    -e SECRET_KEY="$SECRET_KEY" \
    -e FLASK_ENV=production \
    aikaraoke:latest
  
  # Test health endpoint in another terminal
  curl http://localhost:5000/health
  ```

- [ ] **Push to Registry** (optional, for production)
  ```bash
  docker login registry.example.com
  docker tag aikaraoke:latest registry.example.com/aikaraoke:latest
  docker push registry.example.com/aikaraoke:latest
  ```

- [ ] **Image Verification**
  ```bash
  docker images | grep aikaraoke
  docker inspect aikaraoke:latest
  ```

## Docker Compose Deployment

- [ ] **Validate Compose File**
  ```bash
  docker-compose config
  ```

- [ ] **Start Services**
  ```bash
  docker-compose up -d
  ```

- [ ] **Verify Services Running**
  ```bash
  docker-compose ps
  docker-compose logs web  # Check for errors
  ```

- [ ] **Test Health Endpoint**
  ```bash
  docker-compose exec web curl http://localhost:5000/health
  ```

- [ ] **Test Application Access**
  ```bash
  curl http://localhost:5000/
  # Should return HTML home page
  ```

## Reverse Proxy Setup (Nginx)

- [ ] **Enable Nginx Service** (uncomment in docker-compose.yml)

- [ ] **SSL Certificates**: Obtain SSL/TLS certificates
  ```bash
  # Using Let's Encrypt + Certbot
  mkdir -p ssl
  certbot certonly --standalone -d yourdomain.com
  
  # Copy certificates
  cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ssl/cert.pem
  cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ssl/key.pem
  ```

- [ ] **Nginx Configuration**: Update domain names
  ```bash
  # Edit nginx.conf
  # Replace "yourdomain.com" with your actual domain
  sed -i 's/yourdomain.com/your-actual-domain.com/g' nginx.conf
  ```

- [ ] **Restart Services**
  ```bash
  docker-compose down
  docker-compose up -d
  ```

- [ ] **Test HTTPS**
  ```bash
  curl https://yourdomain.com/health
  # Should return JSON health status
  ```

## Firewall & Network Security

- [ ] **Firewall Rules**: Configure firewall
  ```bash
  # Allow SSH
  sudo ufw allow 22/tcp
  
  # Allow HTTP/HTTPS
  sudo ufw allow 80/tcp
  sudo ufw allow 443/tcp
  
  # Deny all other incoming (except established)
  sudo ufw default deny incoming
  sudo ufw default allow outgoing
  sudo ufw enable
  
  # Verify
  sudo ufw status
  ```

- [ ] **Port Mapping**: Verify only necessary ports exposed
  - [ ] 80/tcp (HTTP) - for Let's Encrypt renewal
  - [ ] 443/tcp (HTTPS) - for application
  - [ ] 5000/tcp (Flask) - internal only (localhost)

- [ ] **Network Isolation**: Container network segregation
  - [ ] Containers only connect via Docker network
  - [ ] External access only through reverse proxy

## Storage & Backups

- [ ] **Volume Permissions**: Set correct permissions
  ```bash
  sudo chown -R 1000:1000 uploads projects logs
  sudo chmod 755 uploads projects logs
  ```

- [ ] **Disk Space Monitoring**: Set up monitoring
  ```bash
  # Check available space
  df -h /
  
  # Monitor disk usage
  du -sh uploads projects logs
  ```

- [ ] **Backup Strategy**: Configure automated backups
  ```bash
  # Daily backup script
  cat > /usr/local/bin/backup-aikaraoke.sh << 'EOF'
  #!/bin/bash
  BACKUP_DIR="/backups"
  PROJECT_DIR="/path/to/aikaraoke/projects"
  DATE=$(date +%Y%m%d_%H%M%S)
  
  mkdir -p $BACKUP_DIR
  tar -czf $BACKUP_DIR/aikaraoke_${DATE}.tar.gz $PROJECT_DIR
  
  # Keep only last 7 days
  find $BACKUP_DIR -name "aikaraoke_*.tar.gz" -mtime +7 -delete
  EOF
  
  chmod +x /usr/local/bin/backup-aikaraoke.sh
  
  # Schedule with cron
  echo "0 2 * * * /usr/local/bin/backup-aikaraoke.sh" | crontab -
  ```

- [ ] **Test Restore Procedure**
  ```bash
  # Verify backup integrity
  tar -tzf backup.tar.gz > /dev/null && echo "Backup OK"
  ```

## Database & Data

- [ ] **Database Initialization**: Initialize database if needed
  ```bash
  docker-compose exec web python3 -c "from database.db import init_db; init_db()"
  ```

- [ ] **Data Migration**: Migrate data if upgrading
  ```bash
  # Backup old data first
  docker-compose exec web bash -c "cp karaoke_studio.db karaoke_studio.db.backup"
  
  # Run migrations
  docker-compose exec web python3 -c "from database.db import migrate; migrate()"
  ```

- [ ] **Test Database Access**
  ```bash
  docker-compose exec web python3 << 'EOF'
  from database.db import get_db
  db = get_db()
  print("Database connection OK")
  EOF
  ```

## Monitoring & Logging

- [ ] **Log Rotation**: Verify log rotation configured
  ```bash
  docker-compose logs web | tail -20
  ```

- [ ] **Health Checks**: Verify ongoing health
  ```bash
  # Continuous monitoring
  watch -n 5 'docker-compose exec web curl -s http://localhost:5000/health | jq'
  ```

- [ ] **Performance Monitoring**: Set up monitoring
  ```bash
  # Real-time stats
  docker stats aikaraoke-studio
  ```

- [ ] **Error Logging**: Check for errors
  ```bash
  docker-compose logs web | grep ERROR
  docker-compose logs web | grep WARNING
  ```

## Security Hardening

- [ ] **SSH Keys**: Disable password authentication (if VPS)
  ```bash
  # Edit /etc/ssh/sshd_config
  # PasswordAuthentication no
  # PermitRootLogin no
  
  sudo systemctl restart ssh
  ```

- [ ] **Fail2Ban**: Install intrusion prevention
  ```bash
  sudo apt-get install fail2ban
  sudo systemctl enable fail2ban
  ```

- [ ] **SSL/TLS**: Verify certificate configuration
  ```bash
  openssl s_client -connect yourdomain.com:443 -showcerts
  ```

- [ ] **Secrets Management**: Verify no secrets in code/logs
  ```bash
  # Verify SECRET_KEY not in environment output
  docker-compose config | grep -i secret_key || echo "Not exposed"
  ```

- [ ] **Docker Security**: Apply best practices
  ```bash
  # Enable user namespace remapping in /etc/docker/daemon.json
  # Set to read-only filesystem for app
  # Enable restart policy
  ```

## Performance Tuning

- [ ] **Resource Limits**: Verify resource limits
  ```bash
  docker inspect aikaraoke-studio | grep -A 10 Resources
  ```

- [ ] **Worker Configuration**: Verify gunicorn workers
  ```bash
  # Check in Dockerfile: should be 4+ for production
  docker logs aikaraoke-studio | grep workers
  ```

- [ ] **Cache Warming**: Pre-warm Demucs model
  ```bash
  # Model loads on first request, pre-warming speeds up first upload
  docker-compose exec web curl http://localhost:5000/api/projects
  ```

- [ ] **Connection Pooling**: Verify connection settings
  ```bash
  # Check Nginx upstream configuration
  grep -A 5 "upstream aikaraoke" nginx.conf
  ```

## Production Verification

- [ ] **Full End-to-End Test**
  ```bash
  # Test upload functionality
  curl -X POST -F "file=@test.mp3" http://yourdomain.com/upload
  
  # Test API access
  curl http://yourdomain.com/api/projects
  
  # Test health check
  curl http://yourdomain.com/health
  ```

- [ ] **Load Testing** (optional)
  ```bash
  # Basic load test with ab or wrk
  ab -n 100 -c 10 http://yourdomain.com/
  ```

- [ ] **Accessibility**: Verify HTTPS works
  ```bash
  # Test SSL grade
  curl -I https://yourdomain.com
  # Should have Strict-Transport-Security header
  ```

- [ ] **Mixed Content**: Verify no mixed content warnings
  ```bash
  # Check browser console for security warnings
  ```

## Post-Deployment

- [ ] **Documentation**: Update team documentation
  - [ ] Deployment procedure documented
  - [ ] Runbook for common issues created
  - [ ] Contact information for on-call support

- [ ] **Monitoring Setup**: Configure ongoing monitoring
  - [ ] Health check endpoint monitored
  - [ ] Error logging reviewed regularly
  - [ ] Performance metrics tracked

- [ ] **Incident Response**: Set up incident response
  - [ ] Escalation procedure documented
  - [ ] Rollback procedure documented
  - [ ] Team notification process established

- [ ] **Scheduled Maintenance**: Plan maintenance windows
  - [ ] Weekly log rotation
  - [ ] Monthly certificate renewal check
  - [ ] Quarterly security updates

- [ ] **Notifications**: Set up alerts
  - [ ] Container restart alerts
  - [ ] Disk space warnings
  - [ ] Health check failures
  - [ ] SSL certificate expiration warnings (30 days)

## Rollback Plan

- [ ] **Previous Image**: Keep previous working image tagged
  ```bash
  docker tag aikaraoke:current aikaraoke:stable
  docker build -t aikaraoke:current .
  ```

- [ ] **Quick Rollback**: Document rollback steps
  ```bash
  # If needed:
  docker-compose down
  docker build -t aikaraoke:latest .  # Remove -t to use stable
  docker-compose up -d
  ```

- [ ] **Data Recovery**: Verify backup restoration
  ```bash
  # Test restore (in separate container)
  docker run -v $(pwd)/backups:/backups aikaraoke:latest \
    tar -xzf /backups/aikaraoke_latest.tar.gz
  ```

## Sign-Off

- [ ] **Deployment Date**: _______________
- [ ] **Deployed By**: _______________
- [ ] **Verified By**: _______________
- [ ] **Notes**: _______________

---

✅ **Deployment Complete!** Your AI Karaoke Music Studio is now running in production.

For ongoing support, monitor logs and health checks regularly:
```bash
docker-compose logs -f web
docker-compose exec web curl http://localhost:5000/health
```
