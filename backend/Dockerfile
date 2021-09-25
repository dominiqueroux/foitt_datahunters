FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD ["app.py"] 