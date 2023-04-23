FROM python:3.10-slim-buster

WORKDIR /app
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    PATH="${PATH}:/root/.local/bin"

RUN apt -q update && apt -q install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-ansi --no-root;
COPY . /app/

CMD ["python3", "sample_process.py"]