FROM python:3.11-slim

# Build arguments (from GitHub Actions)
ARG ADMIN_USER
ARG ADMIN_PASSWORD
ARG SUPABASE_URL
ARG SUPABASE_KEY
ARG AZURE_KEY
ARG AZURE_URL

# Optional: Make them available inside the container as env vars
ENV ADMIN_USER=$ADMIN_USER
ENV ADMIN_PASSWORD=$ADMIN_PASSWORD
ENV SUPABASE_URL=$SUPABASE_URL
ENV SUPABASE_KEY=$SUPABASE_KEY
ENV AZURE_KEY=$AZURE_KEY
ENV AZURE_URL=$AZURE_URL

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

CMD ["python", "-m", "main"]
