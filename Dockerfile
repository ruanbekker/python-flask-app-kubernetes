FROM python:3.8-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY app/boot.sh /src/boot.sh
RUN chmod +x /src/boot.sh
COPY app/requirements.txt /src/requirements.txt

RUN pip3 install -r /src/requirements.txt

ADD app/server.py /src/server.py
ADD app/test_server.py /src/test_server.py
WORKDIR /src
RUN pytest 
ENTRYPOINT ["/src/boot.sh"]
