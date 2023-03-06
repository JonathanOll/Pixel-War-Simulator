import os
import cv2
import numpy as np
from options import *
from PIL import ImageFont, Image, ImageDraw
from time import time


def montage(folder, min_x, max_x, min_y, max_y, delete_old=True):

    f = ImageFont.truetype("img/Proxima Nova Font.otf", 120)

    file = folder + "result.mp4"
    print("generating " + file + " ...")

    file_list = os.listdir(folder)
    if "result.mp4" in file_list : file_list.remove("result.mp4")
    file_list.sort(key=lambda a: int(a.split(".")[0]))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter("result/" + folder_name.split("/")[1] + ".mp4", fourcc, framerate, (width, height))

    last_img = None

    last_print = time()
    last_img_index = -1

    ratio = (max_y - min_y) / (max_x - min_x)

    for i in range(duration*framerate):

        n = int(i*len(file_list)/(framerate*duration))

        if n != last_img_index:

            if time() - last_print > 5:
                print("Generating...", round(100*i/(duration*framerate), 2), "%")
                last_print = time()
            img = np.zeros((height, width, 3), np.uint8)
            
            for j in range(3):
                img[:,:,j] = background_color[2-j]

            frame = cv2.imread(os.path.join(folder, file_list[n]))[min_y:max_y, min_x:max_x]
            frame = cv2.resize(frame, (width, int(width * ratio)))

            img[int(height/2-int(width * ratio)/2):int(height/2+int(width * ratio)/2),:] = frame

            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            _, _, text_w, _ = draw.textbbox((0, 0), top_text, font=f)
            draw.text((int(1080/2-text_w/2), 200), top_text, font=f, fill=(255, 255, 255, 255))

            total_y = 0

            for j in range(len(bottom_text)):
                _, _, text_w, text_h = draw.textbbox((0, 0), bottom_text[j], font=f)
                draw.text((int(1080/2-text_w/2), 1450+total_y), bottom_text[j], font=f, fill=(255, 255, 255, 255))
                total_y += text_h

            img = np.array(img_pil)

            last_img = img

            last_img_index = n

        else:
            
            img = last_img

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
