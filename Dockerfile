FROM python:3.12-slim AS base
RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc openssl
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.sh .
COPY ./app/ ./bot

FROM base AS run
RUN chmod +x run.sh
ENTRYPOINT ["/app/run.sh"]

FROM base AS test
COPY ./infra/.env.example ./bot/.env
COPY setup.cfg .
COPY pyproject.toml .
RUN pip install mypy
RUN pip install flake8
#CMD ["python", "-m", "mypy", "."]
CMD ["python", "-m", "flake8", "."]
