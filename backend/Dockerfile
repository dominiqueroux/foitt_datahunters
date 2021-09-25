FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./app/requirements.txt /app/requirements.txt
VOLUME ["/app"]
WORKDIR /app
# We copy just the requirements.txt first to leverage Docker cache
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD ["app.py"] 