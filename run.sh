#!/bin/bash

# Personalized Multimodal AI Digital Assistant - Run Script

echo "Starting Personalized Multimodal AI Digital Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if avatar images exist, create placeholders if not
if [ ! -f "static/images/avatar.png" ] || [ ! -f "static/images/user-avatar.png" ]; then
    echo "Creating placeholder avatar images..."
    mkdir -p static/images
    
    # Try to use ImageMagick if available
    if command -v convert &> /dev/null; then
        convert -size 200x200 xc:white -fill "#4285F4" -draw "circle 100,100 100,50" -pointsize 80 -gravity center -annotate 0 "P" static/images/avatar.png
        convert -size 200x200 xc:white -fill "#FBBC05" -draw "circle 100,100 100,50" -pointsize 80 -gravity center -annotate 0 "U" static/images/user-avatar.png
    else
        # Create empty files if ImageMagick is not available
        touch static/images/avatar.png
        touch static/images/user-avatar.png
        echo "Warning: ImageMagick not found. Created empty avatar files."
    fi
fi

# Run the application
echo "Starting the server..."
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# Deactivate virtual environment on exit
trap "echo 'Deactivating virtual environment...'; deactivate" EXIT