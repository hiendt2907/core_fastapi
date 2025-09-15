# Dockerfile (đặt trong core_fastapi/)
FROM python:3.11-slim

# Set working directory trong container
WORKDIR /app

# Copy requirements.txt từ thư mục hiện tại (nơi Dockerfile đang nằm)
COPY requirements.txt .

# Cài dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Mở port cho Railway
EXPOSE 8000

# Chạy app từ main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

