# Sử dụng base image Python
FROM ubuntu:22.04

RUN apt-get update && apt install -y gunicorn3 python3-pip libpq-dev

# Set working directory trong container
WORKDIR /file-service

COPY requirements.txt .

# Cài đặt các dependencies từ requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Expose cổng mà ứng dụng của bạn chạyz
EXPOSE 5003

# Command để chạy ứng dụng của bạn khi container được khởi chạy
CMD ["python3", "app.py"]