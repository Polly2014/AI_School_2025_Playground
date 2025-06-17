#!/bin/bash
# Development setup script for Multimodal AI Assistant

set -e

echo "🚀 Setting up Multimodal AI Assistant Development Environment"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
    echo "📝 Required: Update LLM_API_KEY and LLM_API_ENDPOINT in .env file"
else
    echo "⚙️ .env file already exists"
fi

# Check if models directory exists
if [ ! -d "models" ]; then
    echo "❌ Models directory not found. Please ensure models/default_profile.json exists."
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Azure OpenAI configuration"
echo "2. Run the application:"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "3. Open http://localhost:8000 in your browser"
echo ""
echo "📚 Documentation:"
echo "   - README.md - General information"
echo "   - CONFIG.md - Configuration guide"
echo "   - DEPLOYMENT.md - Deployment guide"
