FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

WORKDIR /app/src/

EXPOSE 8080
CMD ["gunicorn", "run:app", "--config", "gunicorn_config.py"]