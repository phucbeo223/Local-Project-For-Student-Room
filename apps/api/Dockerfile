FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# psycopg[binary] needs no build deps; keep image slim
COPY requirements*.txt ./
ARG INSTALL_ML=false
RUN pip install --no-cache-dir -r requirements-risk.txt && if [ "$INSTALL_ML" = "true" ]; then pip install --no-cache-dir -r requirements-ml.txt; fi

COPY app ./app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
