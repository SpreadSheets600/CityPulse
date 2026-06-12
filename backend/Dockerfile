FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir uv && \
    uv sync --frozen --no-dev

# NOTE: nvidia/LocateAnything-3B (~6GB) is downloaded at runtime on first startup.
# To pre-download at build time (increases image size significantly), uncomment:
# RUN uv run python -c "from transformers import pipeline; pipeline('image-text-to-text', model='nvidia/LocateAnything-3B', trust_remote_code=True)"

COPY . .

EXPOSE 5000

CMD ["uv", "run", "gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:create_app()"]
