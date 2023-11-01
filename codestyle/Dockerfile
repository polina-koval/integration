FROM python:3.12-slim

VOLUME /code
WORKDIR /codestyle

COPY requirements.txt .
RUN apt-get update -q \
  && apt-get install --no-install-recommends -qy \
  gcc \
    inetutils-ping \
  && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["./entrypoint.sh"]
