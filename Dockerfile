FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variable for persistent data volume
ENV DATA_DIR=/app/data

# Run the server
CMD ["python", "server.py"]
