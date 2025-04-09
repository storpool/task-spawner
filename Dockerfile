FROM python:3.11-slim

# Install tini
RUN apt-get update && apt-get install -y tini && apt-get clean

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/

# Set tini as the init process
ENTRYPOINT ["/usr/bin/tini", "--"]

# Run with Gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app", "--workers=4", "--threads=2"]

# Expose port
EXPOSE 5000
