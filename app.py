import os
import json
import base64
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
import uuid
from pydantic import BaseModel
import logging
from dotenv import load_dotenv
from openai import AzureOpenAI
from models.profile_model import ProfileModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app_title = os.getenv("APP_TITLE", "Multimodal AI Assistant")
app = FastAPI(title=app_title)

# CORS settings
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"]
cors_credentials = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Configure via environment variables
    allow_credentials=cors_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Load profile model
profile_model = ProfileModel("models/default_profile.json")

# Load configuration from environment variables
API_KEY = os.getenv("LLM_API_KEY")
LLM_API_ENDPOINT = os.getenv("LLM_API_ENDPOINT")
VISION_MODEL = os.getenv("VISION_MODEL", "gpt-4o")
TEXT_MODEL = os.getenv("TEXT_MODEL", "gpt-4o")
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "30.0"))
VISION_REQUEST_TIMEOUT = float(os.getenv("VISION_REQUEST_TIMEOUT", "60.0"))
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# DALL-E Configuration
DALLE_ENDPOINT = os.getenv("DALLE_ENDPOINT")
DALLE_API_VERSION = os.getenv("DALLE_API_VERSION", "2024-04-01-preview")
DALLE_DEPLOYMENT = os.getenv("DALLE_DEPLOYMENT", "dall-e-3")
DALLE_API_KEY = os.getenv("DALLE_API_KEY", API_KEY)  # Use same key if not specified

# Validate required configuration
if not API_KEY:
    logger.warning("LLM_API_KEY not found in environment variables. API calls will use demo mode.")
if not LLM_API_ENDPOINT:
    logger.warning("LLM_API_ENDPOINT not found in environment variables. API calls will use demo mode.")
if not DALLE_ENDPOINT:
    logger.warning("DALLE_ENDPOINT not found in environment variables. Image generation will use demo mode.")

# Initialize DALL-E client
dalle_client = None
if DALLE_API_KEY and DALLE_ENDPOINT:
    try:
        dalle_client = AzureOpenAI(
            api_version=DALLE_API_VERSION,
            azure_endpoint=DALLE_ENDPOINT,
            api_key=DALLE_API_KEY,
        )
        logger.info("DALL-E client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize DALL-E client: {str(e)}")
        dalle_client = None

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            
    async def send_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
            
    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str

class ImageAnalysisRequest(BaseModel):
    prompt: Optional[str] = "Please describe this image in detail."
    session_id: Optional[str] = None

class ImageGenerationRequest(BaseModel):
    prompt: str
    style: Optional[str] = "vivid"  # "vivid" or "natural"
    quality: Optional[str] = "standard"  # "standard" or "hd"
    size: Optional[str] = "1024x1024"  # "1024x1024", "1792x1024", or "1024x1792"
    session_id: Optional[str] = None

class ImageGenerationResponse(BaseModel):
    image_url: str
    session_id: str
    prompt_used: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Render the home page"""
    ui_theme = profile_model.get_ui_theme()
    assistant_name = profile_model.get_name()
    avatar = profile_model.get_avatar()
    
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request, 
            "assistant_name": assistant_name,
            "avatar": avatar,
            "theme": ui_theme
        }
    )

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle text chat requests"""
    try:
        # Generate system prompt based on profile
        system_prompt = profile_model.get_personality_prompt()
        
        # Create session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Call LLM API
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            # In a real implementation, replace with actual API call
            try:
                response = await client.post(
                    LLM_API_ENDPOINT,
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": TEXT_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": request.message}
                        ],
                        "max_tokens": MAX_TOKENS
                    }
                )
                
                # For demo purposes, simulate a response if API call fails
                if response.status_code != 200:
                    logger.warning(f"API call failed with status {response.status_code}. Using simulated response.")
                    # Simulate a response based on the personality
                    return ChatResponse(
                        reply=f"I'm {profile_model.get_name()}, your AI assistant. I'd love to help you with '{request.message}', but I'm currently in demo mode. In a real implementation, I would connect to an LLM API to generate a personalized response.",
                        session_id=session_id
                    )
                
                result = response.json()
                return ChatResponse(
                    reply=result["choices"][0]["message"]["content"],
                    session_id=session_id
                )
                
            except Exception as e:
                logger.error(f"Error calling LLM API: {str(e)}")
                # Fallback response for demo
                return ChatResponse(
                    reply=f"I'm {profile_model.get_name()}, your AI assistant. I'd love to help you with '{request.message}', but I'm currently in demo mode. In a real implementation, I would connect to an LLM API to generate a personalized response.",
                    session_id=session_id
                )
                
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/image-analysis")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form("Please describe this image in detail."),
    session_id: Optional[str] = Form(None)
):
    """Handle image analysis requests"""
    try:
        # Generate system prompt based on profile
        system_prompt = profile_model.get_personality_prompt()
        
        # Create session ID if not provided
        session_id = session_id or str(uuid.uuid4())
        
        # Read the uploaded image
        image_data = await file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Call Vision LLM API
        async with httpx.AsyncClient(timeout=VISION_REQUEST_TIMEOUT) as client:
            # In a real implementation, replace with actual API call
            try:
                response = await client.post(
                    LLM_API_ENDPOINT,
                    headers={"Authorization": f"Bearer {API_KEY}"},
                    json={
                        "model": VISION_MODEL,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                            ]}
                        ],
                        "max_tokens": MAX_TOKENS
                    }
                )
                
                # For demo purposes, simulate a response if API call fails
                if response.status_code != 200:
                    logger.warning(f"API call failed with status {response.status_code}. Using simulated response.")
                    # Simulate a response based on the personality
                    return JSONResponse({
                        "analysis": f"I'm {profile_model.get_name()}, your AI assistant. I can see you've shared an image with me. In a real implementation, I would analyze this image using a vision model and provide a detailed description based on my personality profile.",
                        "session_id": session_id
                    })
                
                result = response.json()
                return JSONResponse({
                    "analysis": result["choices"][0]["message"]["content"],
                    "session_id": session_id
                })
                
            except Exception as e:
                logger.error(f"Error calling Vision LLM API: {str(e)}")
                # Fallback response for demo
                return JSONResponse({
                    "analysis": f"I'm {profile_model.get_name()}, your AI assistant. I can see you've shared an image with me. In a real implementation, I would analyze this image using a vision model and provide a detailed description based on my personality profile.",
                    "session_id": session_id
                })
                
    except Exception as e:
        logger.error(f"Error in image analysis endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/image-generation", response_model=ImageGenerationResponse)
async def generate_image(request: ImageGenerationRequest):
    """Handle image generation requests using DALL-E"""
    try:
        # Generate system prompt based on profile for enhancing user prompt
        system_prompt = profile_model.get_personality_prompt()
        
        # Create session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Enhance the prompt using the assistant's personality
        enhanced_prompt = f"Based on my personality as {profile_model.get_name()}, I'll generate an image with this description: {request.prompt}"
        
        if dalle_client:
            try:
                # Generate image using DALL-E
                result = dalle_client.images.generate(
                    model=DALLE_DEPLOYMENT,
                    prompt=request.prompt,
                    n=1,
                    style=request.style,
                    quality=request.quality,
                    size=request.size
                )
                
                # Extract image URL from response
                image_data = json.loads(result.model_dump_json())
                image_url = image_data['data'][0]['url']
                
                logger.info(f"Image generated successfully for prompt: {request.prompt[:50]}...")
                
                return ImageGenerationResponse(
                    image_url=image_url,
                    session_id=session_id,
                    prompt_used=request.prompt
                )
                
            except Exception as e:
                logger.error(f"Error calling DALL-E API: {str(e)}")
                # Fallback response for demo
                return ImageGenerationResponse(
                    image_url="https://via.placeholder.com/1024x1024/4A90E2/FFFFFF?text=Image+Generation+Demo+Mode",
                    session_id=session_id,
                    prompt_used=request.prompt
                )
        else:
            # Demo mode response
            logger.info("DALL-E client not available, using demo mode")
            return ImageGenerationResponse(
                image_url=f"https://via.placeholder.com/1024x1024/4A90E2/FFFFFF?text=Generated:+{request.prompt.replace(' ', '+')[:20]}",
                session_id=session_id,
                prompt_used=request.prompt
            )
                
    except Exception as e:
        logger.error(f"Error in image generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            
            # Parse the received data
            try:
                message_data = json.loads(data)
                user_message = message_data.get("message", "")
                session_id = message_data.get("session_id", client_id)
                
                # Generate system prompt based on profile
                system_prompt = profile_model.get_personality_prompt()
                
                # Process the message (in a real implementation, call the LLM API)
                # For demo, we'll use a simulated response
                assistant_response = f"I'm {profile_model.get_name()}, your AI assistant. In a real-time WebSocket connection, I would process your message: '{user_message}' and respond based on my personality profile."
                
                # Send the response back to the client
                await manager.send_message(
                    json.dumps({
                        "reply": assistant_response,
                        "session_id": session_id
                    }),
                    client_id
                )
                
            except json.JSONDecodeError:
                await manager.send_message(
                    json.dumps({
                        "error": "Invalid JSON format",
                        "session_id": client_id
                    }),
                    client_id
                )
                
    except WebSocketDisconnect:
        manager.disconnect(client_id)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # Use configuration from environment variables
    uvicorn.run(
        app, 
        host=SERVER_HOST, 
        port=SERVER_PORT,
        reload=DEBUG_MODE
    )