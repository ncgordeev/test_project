FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    curl -sSL https://install.python-poetry.org/ | python3 - && \
    apt-get remove -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app/

CMD ["poetry", "run", "python",  "src/manage.py", "runserver", "0.0.0.0:80"]