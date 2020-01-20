FROM python:3.7

RUN pip install uwsgi

ADD requirements.txt ./app/
ADD app.py ./app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["uwsgi", "--socket", "0.0.0.0:3031", "--wsgi-file", "/app/app.py", "--callable", "app", "--processes", "4", "--threads", "2"]
