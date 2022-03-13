FROM ubuntu:20.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list && \
    apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y lib32z1 xinetd

RUN apt-get install -y python3.8 python3-pip
RUN pip install numpy

RUN useradd -m ctf

WORKDIR /home/ctf

RUN mkdir /home/ctf/bin
RUN cp /bin/sh /home/ctf/bin/sh

COPY ./chopsticks.xinetd /etc/xinetd.d/chopsticks
COPY ./start.sh /start.sh
RUN echo "Blocked by xinetd" > /etc/banner_fail

RUN chmod +x /start.sh

COPY ./flag.py /home/ctf/flag.py
COPY ./server.py /home/ctf/server.py
COPY ./strat.py /home/ctf/strat.py
COPY ./p0_perfect.strat /home/ctf/p0_perfect.strat
COPY ./p1_perfect.strat /home/ctf/p1_perfect.strat

CMD ["/home/ctf/bin/sh", "/start.sh"]

EXPOSE 9999
