FROM python:3.10-slim

# Prevents Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures logs are flushed directly
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (minimal)
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (for layer caching)
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy full project
COPY . .

# Install your package
RUN pip install .

# Expose Gradio port
EXPOSE 7860

# Start your app
CMD ["python", "mcp_client.py"]
