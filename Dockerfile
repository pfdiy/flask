FROM python:3.7.4-slim
LABEL author="鸡你太美"

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt

COPY . /usr/src/app

CMD ["gunicorn","-c","/usr/src/app/gunicorncfg.py","wsgi:app"]





