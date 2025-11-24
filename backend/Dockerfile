FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema para numpy, opencv y scikit-image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libsm6 \
    libxext6 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar Python deps sin cache
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "cd app && uvicorn main:app --host 0.0.0.0 --port 8000"]
