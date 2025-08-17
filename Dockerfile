FROM python:3.9-slim

# Install system deps (gcc, portaudio for PyAudio, espeak for pyttsx3)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libportaudio2 \
    portaudio19-dev \
    espeak \
    espeak-ng \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Start Django with Gunicorn
CMD gunicorn AiVoice.wsgi:application --bind 0.0.0.0:$PORT
