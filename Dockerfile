FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
COPY setup.py .

# Install dependencies and package in development mode
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e .

# Copy the rest of the application
COPY . .

# Set PYTHONPATH to include the app directory
ENV PYTHONPATH="${PYTHONPATH}:/app"

# The main application to run
CMD ["python", "main.py"]
