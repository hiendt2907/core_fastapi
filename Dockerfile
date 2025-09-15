# core_fastapi/Dockerfile
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install dependencies
COPY core_fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app code
COPY core_fastapi/ .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

