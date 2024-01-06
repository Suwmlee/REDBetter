FROM python:2-slim

RUN apt-get update \
  && apt-get install -y libjpeg-dev zlib1g-dev \
  && apt-get install -y musl lame sox flac mktorrent \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ADD requirements.txt /app

RUN pip install -r requirements.txt

ADD . /app

USER nobody

CMD ["/app/redactedbetter"]
