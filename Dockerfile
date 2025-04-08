FROM python:3.11-slim

# Set working directory to app source
WORKDIR /app

# Copy only application code, not Helm chart
COPY src/ /app/

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set default command
CMD ["python", "run.py"]
