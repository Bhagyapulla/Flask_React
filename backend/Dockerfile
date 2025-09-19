# Use official Python image
FROM python:3.10-slim

# Install system dependencies (Potrace)
RUN apt-get update && apt-get install -y potrace && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Run Flask app with Gunicorn (production-ready)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
