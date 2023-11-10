FROM python:3.11

WORKDIR /var/www/omo_ws

COPY . /var/www/omo_ws/

ENV PYTHONPATH "${PYTHONPATH}:/var/www/"

RUN pip install --no-cache-dir -r /var/www/omo_ws/requirements.txt

CMD ["uvicorn", "main:handler", "--reload", "--host", "0.0.0.0", "--port", "80"]
