FROM python:3.12
WORKDIR /app

COPY README.md .
COPY models.py .
COPY scrape.py .
COPY pyproject.toml .
COPY uv.lock .
COPY pytest.ini .
COPY run_tests.py .

# Copy test files
COPY tests/ ./tests/

RUN mkdir /app/data
RUN mkdir /app/logs

RUN pip install uv
RUN uv sync

