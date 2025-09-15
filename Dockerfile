# core_fastapi/Dockerfile
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /root/core_fastapi

# Copy requirements and install dependencies
COPY /root/core_fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire app code
COPY /root/core_fastapi/ .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

