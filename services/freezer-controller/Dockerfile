FROM python:3.12-slim

LABEL maintainer="Priyanka Sagalgile"
LABEL project="FinGuard Deployment Freezer"
LABEL service="freezer-controller"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=container

WORKDIR /app

RUN addgroup --system finguard && adduser --system --ingroup finguard finguard

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

RUN chown -R finguard:finguard /app

USER finguard

EXPOSE 8010

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/health').read()" || exit 1

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010"]
