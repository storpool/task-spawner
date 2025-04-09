FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/

# Expose port
EXPOSE 5000

# Run with Gunicorn in production
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app", "--workers=4", "--threads=2"]