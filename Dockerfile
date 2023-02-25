FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt update && apt install default-libmysqlclient-dev build-essential -y
RUN pip install mysqlclient

COPY app/boot.sh /src/boot.sh
RUN chmod +x /src/boot.sh
COPY app/requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

ADD app/*.py /src/
WORKDIR /src
RUN pytest 

ENTRYPOINT ["/src/boot.sh"]
