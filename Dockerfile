FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories if they don't exist
RUN mkdir -p static/images

# Create placeholder avatar images if they don't exist
RUN if [ ! -f "static/images/avatar.png" ]; then \
        touch static/images/avatar.png; \
    fi && \
    if [ ! -f "static/images/user-avatar.png" ]; then \
        touch static/images/user-avatar.png; \
    fi

# Expose the port
EXPOSE 8000

# Set environment variables
ENV LLM_API_KEY=demo_key
ENV LLM_API_ENDPOINT=https://api.example.com/v1/chat/completions
ENV VISION_MODEL=gpt-4-vision-preview
ENV TEXT_MODEL=gpt-4

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]