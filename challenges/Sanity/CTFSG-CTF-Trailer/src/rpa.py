import pyautogui as auto
import os, time

import os
from pathlib import Path
os.chdir(Path(__file__).parent)

auto.hotkey("alt", "tab")
time.sleep(1)
frame = 546

dir = "./out"
if not os.path.isdir(dir):
    os.path.mkdir(dir)

while True:

    auto.press("w")
    brkpt = True
    while brkpt:
        brkpt = auto.locateOnScreen("anchors/resize-dark.JPG", confidence=.8)

    time.sleep(1)
    auto.screenshot("out/frame%d.png"%frame)
    print(f"Frame {frame}!")

    auto.press("F9")
    time.sleep(.5)

    brkpt = None
    while not brkpt:
        brkpt = auto.locateOnScreen("anchors/Breakpoint-dark.JPG", confidence=.8)

    auto.press("enter")
    time.sleep(.5)

    brkpt = None
    while not brkpt:
        brkpt = auto.locateOnScreen("anchors/Breakpoint2-dark.JPG", confidence=.8)

    auto.press("enter")
    time.sleep(1)

    frame += 1