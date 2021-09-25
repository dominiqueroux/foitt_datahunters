FROM ubuntu:20.10 as builder
RUN apt update && apt install -y curl git unzip xz-utils zip libglu1-mesa openjdk-8-jdk wget python3
RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user



#Installing Flutter SDK
RUN git clone https://github.com/flutter/flutter.git
ENV PATH "$PATH:/home/user/flutter/bin"
RUN flutter channel stable
RUN flutter upgrade
VOLUME [ "/home/user/app" ]
EXPOSE 8000
WORKDIR /home/user/app
USER root
ENV PATH "$PATH:/home/user/flutter/bin"
ENTRYPOINT [ "bash" ]
CMD ["bootstrap.sh"] 


