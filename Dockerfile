FROM python:3.7

RUN pip install uwsgi

ADD requirements.txt ./app/
RUN pip install -r /app/requirements.txt

ADD app.py ./app/

WORKDIR /app

CMD ["uwsgi", "--socket", "0.0.0.0:3031", "--wsgi-file", "/app/app.py", "--callable", "app", "--processes", "4", "--threads", "2"]
