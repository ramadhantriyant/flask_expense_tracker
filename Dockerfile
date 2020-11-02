FROM python:3.8.6-buster

WORKDIR /usr/src/app

COPY . .

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "uwsgi", "--socket", "0.0.0.0:5000", "--protocol=http", "-w", "wsgi:app" ]
