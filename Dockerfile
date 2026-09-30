FROM python:3.11-slim

WORKDIR /app

# Instalacja zależności systemowych (ffmpeg i libffi)
RUN apt-get update && apt-get install -y ffmpeg libffi-dev libsodium-dev && rm -rf /var/lib/apt/lists/*

# Kopiowanie i instalacja bibliotek Pythona
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Kopiowanie reszty kodu bota
COPY . .

# Uruchomienie bota
CMD ["python", "bot.py"]
