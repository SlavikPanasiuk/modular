FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3-pip python3-dev

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV UVICORN_CMD="uvicorn main:app --host 0.0.0.0 --port 8000"

CMD [ "sh", "-c", "$UVICORN_CMD" ]