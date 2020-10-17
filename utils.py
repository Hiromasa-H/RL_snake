import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import cv2
import numpy as np
import glob
import sys

def plot_results(x, scores,avg_scores, eps_history, path="latest.png"):
    # episodes = list(range(1,num_episodes+1))

    fig, ax1 = plt.subplots()
    color = 'tab:red'

    ax1.set_xlabel('episodes')
    ax1.set_ylabel('score', color=color)
    ax1.plot(x, scores, color=color)
    ax1.plot(x, avg_scores, color='tab:green')
    # ax1.set_xticks(np.arange(0, num_episodes+1, 100)) 
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('epsilon', color=color)  # we already handled the x-label with ax1
    ax2.plot(x, eps_history, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
    fig.savefig(path,dpi=200)

def save_mp4(frames_path,save_to="latest.mp4",stop_at="XXXXX"):
    print("collecting image frames...")
    img_array = []
    cntr = 0
    for filename in glob.glob(f'{frames_path}/*.jpg'):
        if cntr % 1800 == 0: #30 fps, 1800 frames per min
            print(f"collected {cntr/1800} minutes worth of frames. frame name is: {filename}")
        if stop_at in str(filename):
            break
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        cntr += 1
 
    out = cv2.VideoWriter(save_to,cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
    
    print("making video...")
    for i in range(len(img_array)):
        sys.stdout.write('\r')
        sp = i/((len(img_array)-1)/100)
        tp = int(sp/4)
        sys.stdout.write("[%-25s] %d%%" % ('='*tp, sp)) #25s=25spaces
        sys.stdout.flush()
        out.write(img_array[i])
    out.release()
    print("video is done")