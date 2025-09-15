# Dockerfile
FROM python:3.11-slim

# Set working directory to core_fastapi
WORKDIR /app/core_fastapi

# Install dependencies
COPY core_fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY core_fastapi .

# Expose port
EXPOSE 8000

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

