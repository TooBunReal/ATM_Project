
FROM ubuntu:22.04 as apt-deps

RUN apt-get update && apt install -y gunicorn3 python3-pip libpq-dev
FROM ubuntu:22.04

COPY --from=apt-deps / /

WORKDIR /feedback-service

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5001
CMD ["python3", "app.py"]