import cv2
import os
from pathlib import Path
from PIL import Image
os.chdir(Path(__file__).parent)

images = sorted(["out/"+i for i in os.listdir("out")], key=lambda x: int(x.split(".")[0][9:]))
frames = [cv2.imread(i) for i in images]
frames = [f[25:-40,:] for f in frames]
#Image.fromarray(frames[0]).save("tmp.png"); exit(0)

h,w,l = frames[0].shape
video = cv2.VideoWriter("dist/IDAVid-mid.mp4", 0, 30, (w,h))

for f in frames:
    video.write(f)

cv2.destroyAllWindows()
video.release()