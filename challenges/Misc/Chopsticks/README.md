# Chopsticks

A simplified game of Chopsticks with a player with the best losing strategy (against a random player).

# Description (public)

```
Hey remember that hand game thing called chopsticks?
Pat's pretty good at a modified version of it.
Can you win?

`nc <ip> <port>`
```

# Dependencies  

* Docker engine

# Setup Guide

Update public description with the IP and Port

Move into the `./src` folder and run:

```
dos2unix **
docker build -t chopsticks .
docker run -d -p "0.0.0.0:<port>:9999" -h "chopsticks" --name="chopsticks" chopsticks
```

Give players the port and server-ip to access the challenge

# Solution

The game's pretty simple, players can probably figure out a winning strategy by hand.

# Flag

`CTFSG{Th3_Perf3cT_Pl4YeR_0j2nlhe}`