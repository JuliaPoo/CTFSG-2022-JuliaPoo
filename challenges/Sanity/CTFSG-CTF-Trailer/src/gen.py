import cv2
import numpy as np
from PIL import Image

import os
from pathlib import Path
os.chdir(Path(__file__).parent)

IMAGE_WIDTH = 53
IMAGE_HEIGHT = 30

def parse_video(fn:str):

    video = cv2.VideoCapture(fn)
    s, image = video.read()
    frames = []
    while s: 
        frames.append(image)
        s, image = video.read()

    frames = [
        (np.array(
            Image.fromarray(i)
                .convert("L")
                .resize((IMAGE_WIDTH, IMAGE_HEIGHT))
        )
        .astype(float)/256*25 + 0.5)
        .astype(int)
        .T
        for i in frames
    ]
    return frames

def _make_frame(idx, frame):
    return f"""
void frame{idx}()
{{
	unsigned int i = 0;
	__asm xor esi, esi
	__asm xor edi, edi
    __asm int 3

	switch (i) {{
    {
        chr(10).join(
            f"case {i}: {''.join('P(%d)'%p for p in frame[i])} E;" for i in range(IMAGE_WIDTH)
        )
    }
	case {IMAGE_WIDTH}: {"PAD "*IMAGE_HEIGHT}E;
	default: E;
	}}
end:
	return;
}}
    """

def _make_movie(frames):
    return f"""
void movie()
{{
    {"".join("frame%d();"%i for i in range(len(frames)))}
}}
    """

def make_template(frames):
    return f"""
#pragma once

#include "../image.h"
#define E __asm jmp end

{chr(10).join(_make_frame(i,f) for i,f in enumerate(frames))} 

{_make_movie(frames)}
    """

frames = parse_video('./rsrc/ctfsg-trailer-com.mp4')
template = make_template(frames)

open("IDAVid/cpp/gen/image.h", "w").write(template)