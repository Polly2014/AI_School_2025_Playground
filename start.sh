#!/bin/bash
# Quick start script for Multimodal AI Assistant

echo "🚀 Starting Multimodal AI Assistant..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Start the application
echo "🌟 Starting the application..."
echo "📍 Server will be available at: http://localhost:8000"
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

python app.py
