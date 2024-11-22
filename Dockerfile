FROM python:3.12-slim AS base
RUN apt-get update && apt-get upgrade -y && apt-get install -y libpq-dev gcc openssl
RUN python -m pip install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app/ ./bot

FROM base AS run
COPY run.sh .
RUN chmod +x run.sh
ENTRYPOINT ["/app/run.sh"]

FROM base AS test
COPY ./infra/.env.example ./bot/.env
COPY setup.cfg .
COPY pyproject.toml .
RUN pip install mypy flake8 types-beautifulsoup4 types-html5lib types-PyYAML types-requests
RUN mypy . && flake8 .
