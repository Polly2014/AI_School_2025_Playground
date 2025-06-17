# Configuration Guide

This document provides detailed information about configuring the Multimodal AI Assistant.

## Environment Variables

### Core LLM Configuration

#### LLM_API_KEY
- **Type**: String (Required)
- **Description**: Your Azure OpenAI API key
- **Example**: `9slwOhpI1zBV3YiAgcaD46ZeeHVR39WOiDVAXTk6ln7gIpiWONciJQQJ99BAACHYHv6XJ3w3AAAAACOGHNCK`
- **Security**: Never commit this to version control

#### LLM_API_ENDPOINT
- **Type**: URL (Required)
- **Description**: Azure OpenAI endpoint URL with deployment and API version
- **Format**: `https://{resource}.openai.azure.com/openai/deployments/{deployment}/chat/completions?api-version={version}`
- **Example**: `https://ai-267162017533ai503131807001.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2025-01-01-preview`

#### VISION_MODEL
- **Type**: String
- **Default**: `gpt-4o`
- **Description**: Model name for image analysis tasks
- **Supported Values**: `gpt-4o`, `gpt-4-turbo`, `gpt-4-vision-preview`

#### TEXT_MODEL
- **Type**: String
- **Default**: `gpt-4o`
- **Description**: Model name for text chat tasks
- **Supported Values**: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`

### Server Configuration

#### SERVER_HOST
- **Type**: String
- **Default**: `0.0.0.0`
- **Description**: Host address for the server
- **Options**: 
  - `0.0.0.0` - Listen on all interfaces
  - `127.0.0.1` - Listen only on localhost
  - `localhost` - Listen only on localhost

#### SERVER_PORT
- **Type**: Integer
- **Default**: `8000`
- **Description**: Port number for the server
- **Range**: 1024-65535 (recommended: avoid system ports)

#### DEBUG_MODE
- **Type**: Boolean
- **Default**: `false`
- **Description**: Enable debug mode for development
- **Values**: `true`, `false`
- **Warning**: Never enable in production

### Application Settings

#### APP_TITLE
- **Type**: String
- **Default**: `Multimodal AI Assistant`
- **Description**: Title displayed in the application
- **Usage**: Shown in browser title and UI headers

#### MAX_TOKENS
- **Type**: Integer
- **Default**: `500`
- **Description**: Maximum tokens for LLM responses
- **Range**: 1-4096 (depends on model)
- **Impact**: Higher values = longer responses, higher API costs

#### REQUEST_TIMEOUT
- **Type**: Float
- **Default**: `30.0`
- **Description**: Timeout for text API requests (seconds)
- **Range**: 5.0-300.0
- **Recommendation**: 30-60 seconds for production

#### VISION_REQUEST_TIMEOUT
- **Type**: Float
- **Default**: `60.0`
- **Description**: Timeout for vision API requests (seconds)
- **Range**: 10.0-300.0
- **Note**: Vision requests typically take longer

### Security and CORS

#### ALLOWED_ORIGINS
- **Type**: String (comma-separated)
- **Default**: `*`
- **Description**: CORS allowed origins
- **Development**: `*` (allow all)
- **Production**: Specific domains only
- **Example**: `https://app.example.com,https://www.example.com`

#### CORS_CREDENTIALS
- **Type**: Boolean
- **Default**: `true`
- **Description**: Allow credentials in CORS requests
- **Values**: `true`, `false`
- **Security**: Set to `false` if not needed

## Profile Configuration

### Location
The personality profile is stored in `models/default_profile.json`.

### Structure

```json
{
  "basic_info": {
    "name": "Assistant Name",
    "age": 25,
    "gender": "neutral",
    "role": "AI Assistant",
    "personality_description": "Description of personality",
    "knowledge_domains": ["technology", "science", "general"],
    "communication_style": "friendly"
  },
  "psychological_profile": {
    "openness": 0.8,
    "conscientiousness": 0.9,
    "extraversion": 0.7,
    "agreeableness": 0.8,
    "emotional_stability": 0.9
  },
  "behavioral_patterns": {
    "response_length": "medium",
    "formality_level": "casual",
    "use_emojis": true,
    "ask_clarifying_questions": true,
    "provide_examples": true
  },
  "ui_theme": {
    "primary_color": "#4A90E2",
    "secondary_color": "#F5F5F5",
    "accent_color": "#FF6B6B",
    "theme_mode": "auto"
  },
  "avatar": {
    "style": "modern",
    "color_scheme": "blue",
    "expression": "friendly"
  }
}
```

### Customization Guidelines

#### Psychological Traits (0.0 - 1.0 scale)

- **Openness**: Creativity and openness to new experiences
  - Low (0.0-0.3): Conservative, traditional
  - Medium (0.4-0.7): Balanced approach
  - High (0.8-1.0): Creative, adventurous

- **Conscientiousness**: Organization and dependability
  - Low (0.0-0.3): Casual, spontaneous
  - Medium (0.4-0.7): Moderately organized
  - High (0.8-1.0): Highly organized, detail-oriented

- **Extraversion**: Social energy and assertiveness
  - Low (0.0-0.3): Reserved, quiet
  - Medium (0.4-0.7): Balanced social interaction
  - High (0.8-1.0): Outgoing, energetic

- **Agreeableness**: Cooperation and trust
  - Low (0.0-0.3): Direct, competitive
  - Medium (0.4-0.7): Balanced approach
  - High (0.8-1.0): Cooperative, trusting

- **Emotional Stability**: Emotional resilience
  - Low (0.0-0.3): Sensitive, reactive
  - Medium (0.4-0.7): Generally stable
  - High (0.8-1.0): Very calm, stable

#### Response Patterns

- **Response Length**: `short`, `medium`, `long`
- **Formality Level**: `formal`, `casual`, `mixed`
- **Communication Style**: `friendly`, `professional`, `enthusiastic`, `calm`

## Advanced Configuration

### Custom Model Endpoints

For non-Azure OpenAI endpoints, modify the API call format in `app.py`:

```python
# Custom endpoint configuration
CUSTOM_API_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Custom-Header": "value"  # Add custom headers if needed
}

# Modify request format if needed
api_request = {
    "model": TEXT_MODEL,
    "messages": messages,
    "max_tokens": MAX_TOKENS,
    # Add custom parameters here
}
```

### Logging Configuration

Add to your `.env` file:

```env
# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
LOG_FILE=app.log
LOG_MAX_SIZE=10485760  # 10MB
LOG_BACKUP_COUNT=5
```

### Performance Tuning

```env
# Performance Settings
WORKER_COUNT=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
KEEP_ALIVE=2
MAX_REQUESTS=1000
MAX_REQUESTS_JITTER=100

# Connection Pool Settings
CONNECTION_POOL_SIZE=10
CONNECTION_POOL_MAXSIZE=20
```

## Configuration Validation

The application validates configuration on startup:

1. **Required Variables**: Checks for LLM_API_KEY and LLM_API_ENDPOINT
2. **Type Validation**: Ensures numeric values are valid
3. **Range Validation**: Checks timeout values are reasonable
4. **URL Validation**: Validates endpoint URL format

### Validation Errors

Common configuration errors:

- **Missing API Key**: Application starts in demo mode
- **Invalid Endpoint**: API calls will fail
- **Invalid Timeouts**: Defaults will be used
- **Invalid Port**: Application will fail to start

## Environment-Specific Configurations

### Development (.env.development)
```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
SERVER_HOST=localhost
SERVER_PORT=8000
ALLOWED_ORIGINS=*
REQUEST_TIMEOUT=10.0
```

### Testing (.env.testing)
```env
DEBUG_MODE=false
LOG_LEVEL=INFO
SERVER_HOST=localhost
SERVER_PORT=8001
ALLOWED_ORIGINS=http://localhost:3000
MAX_TOKENS=100
```

### Production (.env.production)
```env
DEBUG_MODE=false
LOG_LEVEL=WARNING
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ALLOWED_ORIGINS=https://yourdomain.com
CORS_CREDENTIALS=true
REQUEST_TIMEOUT=60.0
MAX_TOKENS=1000
```

## Configuration Management Best Practices

1. **Use Environment-Specific Files**: Separate configurations for dev/test/prod
2. **Version Control**: Include `.env.example`, exclude actual `.env` files
3. **Validation**: Always validate configuration on application startup
4. **Documentation**: Keep this guide updated with new configuration options
5. **Security**: Use secure methods for sensitive configuration in production
6. **Defaults**: Provide sensible defaults for optional settings
7. **Testing**: Test configuration changes in development first

## Troubleshooting Configuration Issues

### Common Problems

1. **Application won't start**: Check required environment variables
2. **API calls failing**: Verify API key and endpoint
3. **CORS errors**: Check ALLOWED_ORIGINS setting
4. **Slow responses**: Adjust timeout values
5. **Out of memory**: Reduce MAX_TOKENS or worker count

### Debug Configuration

Enable debug logging to troubleshoot:

```env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

Check logs for configuration warnings and errors during startup.
