# Dockerfile (đặt tại /root/core_fastapi)
FROM python:3.11-slim

# Set working directory trong container
WORKDIR /app

# Copy requirements.txt từ thư mục core_fastapi
COPY core_fastapi/requirements.txt .

# Cài dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn từ core_fastapi
COPY core_fastapi/ .

# Mở port cho Railway
EXPOSE 8000

# Chạy app từ main.py trong core_fastapi
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

