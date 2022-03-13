FROM ubuntu:20.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade

RUN apt-get install -y python3.8 python3-pip

RUN useradd -m ctf

WORKDIR /home/ctf

RUN echo "Blocked by blind_xinetd" > /etc/banner_fail

COPY . /home/ctf/
RUN python3 -m pip install -e .

CMD ["python3", "./deploy.py"]

EXPOSE 5555
