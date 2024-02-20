FROM python:3.12-slim
RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc openssl
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.sh .
COPY ./app/ ./bot
RUN chmod +x run.sh
ENTRYPOINT ["/app/run.sh"]
