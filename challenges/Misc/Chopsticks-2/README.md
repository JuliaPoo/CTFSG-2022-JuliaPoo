# Chopsticks 2

The actual chopsticks game but it loops at 7 instead of 5, against a "good enough" player (not perfect).

# Description (public)

```
Oh have you beat Pat in the previous game? Nice!
Well here's the classic chopsticks game, but this time,
it loops at 7 instead of 5!

`nc <ip> <port>`
```

# Dependencies  

* Docker engine

# Setup Guide

Update public description with the IP and Port

Move into the `./src` folder and run:

```
dos2unix **
docker build -t chopsticks2 .
docker run -d -p "0.0.0.0:<port>:9999" -h "chopsticks2" --name="chopsticks2" chopsticks2
```

Give players the port and server-ip to access the challenge

# Solution

Erhhhhhh I mean I can win `Pat` with the same code as `Pat`, but I have no idea how hard it is to manually figure out a strong enough strategy.

# Flag

`CTFSG{Ch0pst!ck5_m4STeR!11!_aim48djam3}`