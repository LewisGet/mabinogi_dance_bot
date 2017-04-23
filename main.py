import cv2
import pyautogui as gui
from PIL import Image
from PIL import ImageGrab
import numpy as np
import time

def get_music_screen_pixel():
    image = ImageGrab.grab()
    image_array = np.array(image, dtype=np.uint8)

    return image_array[569:700, 520:1600]

def get_basic_control_images():
    images = [None] * 4
    
    for i in range(4):
        images[i] = (np.array(Image.open("data/" + str(i + 1) + ".bmp"), dtype=np.uint8))[0:15, 0:15]
    
    return images

def match_command(screen, images):
    command = []
    
    for i, image in enumerate(images):
        command.append(cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED))

    return command

def match_to_list(matches):
    commands = []
    
    a = np.where(matches[0] > 0.95)[1]
    w = np.where(matches[1] > 0.95)[1]
    d = np.where(matches[2] > 0.95)[1]
    s = np.where(matches[3] > 0.95)[1]
    
    for i in range(1100):
        if (i in a):
            commands.append("a")
            
        if (i in d):
            commands.append("d")
            
        if (i in w):
            commands.append("w")
            
        if (i in s):
            commands.append("s")
    
    return commands

command_images = get_basic_control_images()

time.sleep(5)

if __name__ == '__main__':
    for t in range(30 * 60 * 100):
        now_screen = get_music_screen_pixel()
        matches = match_command(now_screen, command_images)
        keys = match_to_list(matches)

        gui.press(keys)
        print(keys)
