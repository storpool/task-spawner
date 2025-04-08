FROM python:3.11-slim

# Set up app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . .

# Default command
CMD ["python", "run.py"]
