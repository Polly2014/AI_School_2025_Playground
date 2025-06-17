# Personalized Multimodal AI Digital Assistant

This project demonstrates a personalized multimodal AI assistant with profile-driven behavior, capable of text chat and image analysis.

## Features

- **Profile-Driven Personalization**: The assistant's behavior is driven by a personality profile that defines traits like openness, conscientiousness, extraversion, agreeableness, and emotional stability.
- **Multimodal Interaction**: Supports both text chat and image analysis.
- **Responsive UI**: Modern, responsive interface with light/dark theme support.
- **Real-time Communication**: Uses REST APIs for communication with the backend.

## Project Structure

```
demo/
├── models/                    # Profile model and default profile
│   ├── profile_model.py       # Profile model implementation
│   └── default_profile.json   # Default personality profile
├── static/                    # Static assets
│   ├── css/                   # CSS styles
│   ├── js/                    # JavaScript files
│   └── images/                # Images and avatars
├── templates/                 # HTML templates
│   └── index.html             # Main application template
├── app.py                     # FastAPI application
├── requirements.txt           # Project dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── setup.sh                  # Setup script (Unix/Linux/Mac)
├── start.sh                  # Quick start script (Unix/Linux/Mac)
├── CONFIG.md                 # Configuration guide
├── DEPLOYMENT.md             # Deployment guide
├── CONTRIBUTING.md           # Contribution guidelines
├── LICENSE                   # MIT License
├── Dockerfile                # Docker configuration
└── docker-compose.yml        # Docker Compose configuration
```

## Technical Architecture

1. **Frontend**: HTML/CSS/JavaScript for the user interface
2. **Backend**: FastAPI for the server
3. **Multimodal Core**: Integration with large language models (LLMs) for text and vision processing
4. **Personalization Engine**: Profile-driven personality model

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Azure OpenAI API access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Polly2014/AI_School_2025_Playground.git
   cd AI_School_2025_Playground/demo
   ```

2. **Set up the environment**
   ```bash
   # Use the setup script for easy installation
   chmod +x setup.sh
   ./setup.sh
   ```
   
   Or manually:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Copy environment template
   cp .env.example .env
   ```

3. **Configure your API keys**
   
   Edit `.env` file and add your Azure OpenAI credentials:
   ```env
   LLM_API_KEY=your_azure_openai_api_key_here
   LLM_API_ENDPOINT=https://your-resource.openai.azure.com/openai/deployments/your-model/chat/completions?api-version=2025-01-01-preview
   ```

4. **Start the application**
   ```bash
   # Quick start
   ./start.sh
   
   # Or manually
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8000`

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_API_KEY` | Azure OpenAI API key | `your_api_key_here` |
| `LLM_API_ENDPOINT` | Azure OpenAI endpoint URL | `https://your-resource.openai.azure.com/...` |

### Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VISION_MODEL` | `gpt-4o` | Model for image analysis |
| `TEXT_MODEL` | `gpt-4o` | Model for text chat |
| `SERVER_HOST` | `0.0.0.0` | Server host address |
| `SERVER_PORT` | `8000` | Server port |
| `DEBUG_MODE` | `false` | Enable debug mode |
| `APP_TITLE` | `Multimodal AI Assistant` | Application title |
| `MAX_TOKENS` | `500` | Maximum tokens for responses |
| `REQUEST_TIMEOUT` | `30.0` | Request timeout in seconds |
| `VISION_REQUEST_TIMEOUT` | `60.0` | Vision request timeout in seconds |
| `ALLOWED_ORIGINS` | `*` | CORS allowed origins (comma-separated) |
| `CORS_CREDENTIALS` | `true` | Enable CORS credentials |

- `LLM_API_KEY`: API key for the LLM service
- `LLM_API_ENDPOINT`: Endpoint URL for the LLM API
- `VISION_MODEL`: Model name for vision tasks (default: "gpt-4-vision-preview")
- `TEXT_MODEL`: Model name for text tasks (default: "gpt-4")

## Customizing the Assistant

You can customize the assistant's personality by modifying the `default_profile.json` file. The profile includes:

- **Basic Attributes**: Name, age, gender, role, knowledge domains, etc.
- **Psychological Traits**: OCEAN personality model (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
- **Behavioral Patterns**: Response patterns and interaction preferences
- **Appearance**: Visual theme and color scheme

## Future Enhancements

1. **WebSocket Support**: Implement real-time communication using WebSockets
2. **Voice Interaction**: Add speech-to-text and text-to-speech capabilities
3. **Memory System**: Implement a conversation memory system for better context awareness
4. **User Profiles**: Allow users to create and switch between different assistant personalities
5. **Advanced Analytics**: Track interaction patterns and adapt the assistant's behavior over time

## License

This project is for educational purposes only.