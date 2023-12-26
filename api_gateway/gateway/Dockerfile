FROM ubuntu:22.04


WORKDIR /fontend-service

COPY requirements.txt .

RUN apt-get update && apt install -y gunicorn3 python3-pip libpq-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn3", "--bind", "0.0.0.0:5000", "fontend-service:app"]
