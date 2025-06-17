FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libzbar0 \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
