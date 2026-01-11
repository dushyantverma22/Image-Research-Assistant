FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy entire project
COPY . .

# Expose Gradio port
EXPOSE 7860

# Run your app
CMD ["python", "mcp_client.py"]
