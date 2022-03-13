# CTF.SG CTF Trailer

# Description (public)

```
[TODO]
```

# Setup Guide

1. Provide files in `dist/` to players

# Build steps

## Building

* Run `gen.py`, modify accordingly
* Open `x64_x86 Cross Tools Command Prompt for VS 2019` (IMPORTANT)
* Run `msbuild /t:IDAVid /property:Configuration=Release /property:Platform="x86"`
* Load into IDA with symbols (a lot faster)
* Configure IDA
    * Disable graph animations
    * Don't display comments and prefixes
* Run the debugger until a breakpoint hits, clean up screen, etc, etc
* Run `rpa.py`

# Flag

`CTFSG{CFG_4n1m4t10n}`