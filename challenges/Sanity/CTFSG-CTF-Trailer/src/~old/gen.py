import cv2
import numpy as np
from PIL import Image

from typing import List

import os
from pathlib import Path
os.chdir(Path(__file__).parent)

IMAGE_WIDTH = 40
IMAGE_HEIGHT = 40

def parse_video(fn:str):

    video = cv2.VideoCapture(fn)
    s, image = video.read()
    frames = []
    while s: 
        frames.append(image)
        s, image = video.read()
    nframes = len(frames)

    frames = [
        np.array(Image.fromarray(i).convert("L").resize((IMAGE_WIDTH, IMAGE_HEIGHT))).T.reshape(-1) 
        for i in frames
    ]
    frames = [int(float(i)/256*25 + 0.5) for j in frames for i in j]
    return nframes, frames

def make_template(W:int,H:int,F:int,P:List[int]):

    template = open("./templates/image.data.template").read()
    template = template.replace("<<N_FRAMES>>", str(F))
    template = template.replace("<<IMAGE_WIDTH>>", str(W))
    template = template.replace("<<IMAGE_HEIGHT>>", str(H))
    template = template.replace("<<MOVIE_PVALS>>", ",".join(map(str,P)))
    
    dir = "./IDAVid/cpp/gen/"
    if not os.path.isdir(dir):
        os.path.mkdir(dir)
    open(dir + "image.data", "w").write(template)


N_FRAMES, MOVIE_PVALS = parse_video('./rsrc/fengshui.gif')
make_template(IMAGE_WIDTH, IMAGE_HEIGHT, N_FRAMES, MOVIE_PVALS)



