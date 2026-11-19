FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    libjpeg62-turbo \
    libpng16-16 \
    netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip --quiet \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

# Create non-root user
RUN addgroup --system django \
 && adduser --system --ingroup django django

# Pre-create writable dirs and hand them to the django user BEFORE any volume mount
RUN mkdir -p /app/staticfiles /app/media \
 && chown -R django:django /app

USER django

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
