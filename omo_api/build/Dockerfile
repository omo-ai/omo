# base stages
FROM python:3.11-slim-bullseye as base-install
RUN apt update
RUN apt install -y tesseract-ocr libcairo2-dev pkg-config python3-dev gcc vim

FROM base-install as base-requirements
COPY requirements.txt /var/www/omo_api/requirements.txt
RUN pip install --no-cache-dir -r var/www/omo_api/requirements.txt

# build stages
FROM base-requirements as build
COPY . /var/www/omo_api/
WORKDIR /var/www/omo_api
ENV PYTHONPATH "${PYTHONPATH}:/var/www/"

# api
FROM build as api
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]

# celery worker
FROM build as celeryworker
CMD ["celery", "-A", "workers.background", "worker", "-l", "debug"]

# celery beat
FROM build as celerybeat
CMD ["celery", "-A", "workers.background", "beat", "-l", "debug"]