# Virtual Try-On System - Docker Deployment

This guide explains how to deploy the Virtual Try-On system using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier management)
- At least 4GB RAM
- 10GB free disk space

## Quick Start

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up --build

# Run in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t vfit2-app .

# Run the container
docker run -p 8000:8000 \
  -v $(pwd)/backend/data/media:/app/backend/data/media \
  -v $(pwd)/logs:/app/logs \
  vfit2-app

# Run in background
docker run -d -p 8000:8000 \
  --name vfit2-container \
  -v $(pwd)/backend/data/media:/app/backend/data/media \
  -v $(pwd)/logs:/app/logs \
  vfit2-app
```

## Access the Application

Once running, access the application at:
- **Local**: http://localhost:8000
- **Network**: http://[server-ip]:8000

## Environment Variables

You can customize the deployment using environment variables:

```bash
# In docker-compose.yml or docker run command
DJANGO_DEBUG=0                    # Set to 1 for debug mode
DJANGO_ALLOWED_HOSTS=*           # Comma-separated list of allowed hosts
BLENDER_BIN=/usr/local/bin/blender # Path to Blender executable
```

## Volume Mounts

The container uses these volumes:
- `./backend/data/media:/app/backend/data/media` - Generated models and media files
- `./logs:/app/logs` - Application logs

## Troubleshooting

### Container won't start
```bash
# Check logs
docker-compose logs
docker logs vfit2-container

# Check if ports are available
netstat -tulpn | grep :8000
```

### Blender issues
```bash
# Exec into container to check Blender
docker exec -it vfit2-container bash
blender --version
```

### Performance issues
- Ensure Docker has at least 4GB RAM allocated
- Close other resource-intensive applications
- Consider using a machine with GPU support for faster processing

### Accessing files
```bash
# Copy files from container
docker cp vfit2-container:/app/backend/data/media ./output

# Exec into container
docker exec -it vfit2-container bash
```

## Production Deployment

For production deployment:

1. **Use a reverse proxy** (nginx, traefik) for SSL and load balancing
2. **Set up proper logging** and monitoring
3. **Configure backups** for the media volume
4. **Use environment-specific settings**
5. **Set up health checks** and restart policies

### Example nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    client_max_body_size 10M;
}
```

## Maintenance

### Update the application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose down
docker-compose up --build -d
```

### Clear cache and data
```bash
# Remove all generated data
docker-compose down
sudo rm -rf backend/data/media/run_*
docker-compose up -d
```

### Backup data
```bash
# Backup generated models
tar -czf backup-$(date +%Y%m%d).tar.gz backend/data/media/
```