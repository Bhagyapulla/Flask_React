# Use official Python image
FROM python:3.10-slim

# Install Potrace
RUN apt-get update && apt-get install -y potrace

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Run Flask
CMD ["python", "app.py"]
