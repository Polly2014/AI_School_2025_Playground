# Deployment Guide

This guide covers deployment options and best practices for the Multimodal AI Assistant.

## Deployment Options

### 1. Local Development

For local development and testing:

```bash
# Clone and setup
git clone <repository-url>
cd demo
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run development server
python app.py
```

### 2. Docker Deployment

The application includes Docker support for containerized deployment.

#### Build and Run with Docker

```bash
# Build the Docker image
docker build -t multimodal-ai-assistant .

# Run the container
docker run -p 8000:8000 --env-file .env multimodal-ai-assistant
```

#### Docker Compose

For a complete deployment with additional services:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 3. Production Deployment

#### Using Uvicorn with Gunicorn

For production deployment, use Gunicorn with Uvicorn workers:

```bash
# Install additional dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Environment Configuration for Production

Create a production `.env` file:

```env
# Production Configuration
LLM_API_KEY=your_production_api_key
LLM_API_ENDPOINT=your_production_endpoint
DEBUG_MODE=false
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Security Settings
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_CREDENTIALS=true

# Performance Settings
MAX_TOKENS=1000
REQUEST_TIMEOUT=60.0
VISION_REQUEST_TIMEOUT=120.0
```

## Security Considerations

### 1. API Key Management

- **Never commit API keys to version control**
- Use environment variables or secure secret management services
- Rotate API keys regularly
- Consider using Azure Key Vault or similar services for production

### 2. CORS Configuration

```env
# Restrict CORS origins in production
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
CORS_CREDENTIALS=true
```

### 3. Rate Limiting

Consider implementing rate limiting for production deployments:

```python
# Example using slowapi
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, chat_request: ChatRequest):
    # Your existing chat logic
    pass
```

## Monitoring and Logging

### 1. Application Logging

The application uses Python's logging module. Configure log levels:

```env
# Add to .env
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### 2. Health Checks

The application includes a health check endpoint:

```
GET /health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-06-17T10:30:00Z",
  "version": "1.0.0"
}
```

### 3. Metrics and Monitoring

For production monitoring, consider integrating:

- **Prometheus**: For metrics collection
- **Grafana**: For visualization
- **Application Insights**: For Azure deployments
- **Sentry**: For error tracking

## Scaling Considerations

### 1. Horizontal Scaling

The application is stateless and can be horizontally scaled:

```yaml
# docker-compose.yml for multiple instances
version: '3.8'
services:
  app:
    image: multimodal-ai-assistant
    replicas: 3
    ports:
      - "8000-8002:8000"
    environment:
      - SERVER_PORT=8000
```

### 2. Load Balancing

Use a reverse proxy like Nginx for load balancing:

```nginx
upstream app_servers {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://app_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Backup and Recovery

### 1. Configuration Backup

Regularly backup your configuration files:

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p backups/$DATE
cp .env backups/$DATE/
cp models/default_profile.json backups/$DATE/
tar -czf backups/config_backup_$DATE.tar.gz backups/$DATE/
```

### 2. Application State

Since the application is stateless, focus on:
- Configuration files backup
- Custom personality profiles
- Any custom templates or assets

## Troubleshooting

### Common Issues

1. **API Connection Issues**
   - Verify API key and endpoint
   - Check network connectivity
   - Review timeout settings

2. **Performance Issues**
   - Monitor request timeout settings
   - Check API rate limits
   - Review server resources

3. **CORS Issues**
   - Verify ALLOWED_ORIGINS setting
   - Check browser developer tools for CORS errors

### Debug Mode

Enable debug mode for troubleshooting:

```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

### Logs Analysis

Monitor application logs for issues:

```bash
# Follow logs in real-time
tail -f app.log

# Search for errors
grep "ERROR" app.log

# Monitor API calls
grep "API call" app.log
```

## Performance Optimization

### 1. Caching

Consider implementing caching for frequently requested content:

```python
# Example using Redis
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_response(key: str):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None

async def cache_response(key: str, data: dict, ttl: int = 300):
    redis_client.setex(key, ttl, json.dumps(data))
```

### 2. Request Optimization

- Use connection pooling for HTTP clients
- Implement request batching where possible
- Optimize timeout values based on your use case

### 3. Resource Management

- Monitor memory usage
- Set appropriate worker counts
- Configure garbage collection if needed

## Updates and Maintenance

### 1. Dependency Updates

Regularly update dependencies:

```bash
# Check for updates
pip list --outdated

# Update requirements
pip-review --local --auto

# Update requirements.txt
pip freeze > requirements.txt
```

### 2. Security Updates

- Monitor security advisories
- Update base Docker images regularly
- Keep API client libraries updated

### 3. Configuration Reviews

Regularly review and update:
- API endpoints and versions
- Security settings
- Performance configurations
- Logging levels
