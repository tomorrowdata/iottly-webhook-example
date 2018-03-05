FROM python:3.6.4
MAINTAINER TomorrowData

EXPOSE 9000

RUN mkdir /app

ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ADD server /app/server
ADD client /app/client

CMD ["python", "/app/server/main.py"]
