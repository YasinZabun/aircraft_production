FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY init.sh /app/

RUN chmod +x /app/init.sh

EXPOSE 8000

ENTRYPOINT ["/app/init.sh"]

CMD ["gunicorn", "aircraft_app.wsgi:application", "--bind", "0.0.0.0:8000"]
