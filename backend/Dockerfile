FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
VOLUME ["/app"]
WORKDIR /app
RUN pip install pipenv
ENTRYPOINT [ "bash" ]
CMD ["/app/bootstrap.sh"] 