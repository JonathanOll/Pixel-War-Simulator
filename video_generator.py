import os
import cv2
import numpy as np
from options import *

def montage(folder, delete_old=True):

    file = folder + "/result.mp4"
    print("generating " + file + " ...")

    file_list = os.listdir(folder)
    if "result.mp4" in file_list : file_list.remove("result.mp4")
    file_list.sort(key=lambda a: int(a.split(".")[0]))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("result/" + folder_name.split("/")[1] + ".mp4", fourcc, framerate, (width, height))

    last_img = None

    for i in range(duration*framerate):
        img = np.zeros((height, width, 3), np.uint8)
        
        for j in range(3):
            img[:,:,j] = background_color[2-j]

        frame = cv2.imread(os.path.join(folder, file_list[int(i*len(file_list)/(framerate*duration))]))[8:8+source_height, 296:296+source_height]
        frame = cv2.resize(frame, (width, width))

        img[int(height/2-width/2):int(height/2+width/2),:] = frame

        last_img = img
        
        video_writer.write(img)

    for i in range(result_duration * framerate):
        video_writer.write(last_img)

    # relâcher les ressources
    video_writer.release()

    if delete_old:
        for f in file_list:
            os.remove(folder + "/" + f)
    os.rmdir(folder_name)

    print('Successfully generated', file, "!")
