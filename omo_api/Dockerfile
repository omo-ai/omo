FROM python:3.11

WORKDIR /var/www/omo_api

COPY . /var/www/omo_api/

ENV PYTHONPATH "${PYTHONPATH}:/var/www/"

RUN apt update
RUN apt install -y tesseract-ocr libcairo2-dev pkg-config

RUN pip install --no-cache-dir -r /var/www/omo_api/requirements.txt

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]