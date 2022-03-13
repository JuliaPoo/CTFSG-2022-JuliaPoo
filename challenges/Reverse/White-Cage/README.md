# White Cage

A heavily obfuscated function that does a string compare with the user input and the flag. Infeasible to reverse, a side channel is intended.

# Description (public)

```
I found this script somewhere in Kebun Baru, it seems to require a password.
```

# Setup Guide

1. Provide files in `dist/` to players

# Solution 1

A side channel via python's `sys.settrace(tracer)`. The string compare function does early stopping, so `tracer` would be fired more times for more correct characters in general.

Experimentation shows if a character is guessed wrong, regardless of the next character, the difference in number of events is less than `1000`. This can be used
to recover the flag character by character.

`pypy3` can be used to speed up the side channel attack, and the flag can be recovered in 5mins. Script in `./sol` folder.

# Solution 2

Realize it is SKI combinators, attempt to extract the string in SKI combinators and pass it through a SKI to lambda compiler for (a lot) better readability.

Reverse the string checking function to know the purpose of of the `2022` and `127` constant, and solve. Script in the `./sol2` folder.

# Flag

`CTFSG{I_respect_Ur_Cunning_BUT_no}`