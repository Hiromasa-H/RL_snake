from utils import save_mp4
import cv2
import numpy as np
import glob
import sys

if __name__ == '__main__':

    frames_path = "frames"
    save_to="results(1/2).mp4"
    start_at = "ep2501"
    stop_at = "XXXXX" #"ep2500"

    # save_mp4(frames_path,save_to)
    print(f"save_to = {save_to}")
    print("collecting image frames...")
    img_array = []
    cntr = 0
    for filename in glob.glob(f'{frames_path}/*.jpg'):
        # print(filename[7:13])
        if cntr % 1800 == 0: #30 fps, 1800 frames per min
            print(f"collected {cntr/1800} minutes worth of frames. frame name is: {filename}")
        if stop_at in str(filename):
            break
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        cntr += 1
    
    out = cv2.VideoWriter(save_to,cv2.VideoWriter_fourcc(*'mp4v'), 30, size)
    
    print("making video...")
    for i in range(len(img_array)):
        sys.stdout.write('\r')
        sp = i/((len(img_array)-1)/100)
        tp = int(sp/4)
        sys.stdout.write("[%-25s] %d%%" % ('='*tp, sp)) #20s=20spaces
        sys.stdout.flush()
        out.write(img_array[i])
    out.release()
    print("video is done")
    
