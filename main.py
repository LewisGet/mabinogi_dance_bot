import cv2
import ctypes
import gui
from PIL import Image
from PIL import ImageGrab
import numpy as np
import time
import os

def get_music_screen_pixel():
    image = ImageGrab.grab()
    image_array = np.array(image, dtype=np.uint8)

    return image_array[569:700, 520:1600]

def get_basic_control_images():
    images = [None] * 4
    
    for i in range(4):
        path = os.sep.join([os.path.expanduser("~lewis"), "Desktop", "code", "denc", "data", str(i + 1) + ".bmp"]);
        images[i] = (np.array(Image.open(path), dtype=np.uint8))[0:15, 0:15]
    
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

def key_press(vm_key, scan):
    key_input = ctypes.windll.user32.keybd_event;
    key_down = 0x0001
    key_up = 0x0002

    key_input(vm_key, scan, key_down)
    time.sleep(0.05)
    key_input(vm_key, scan, key_up)
    time.sleep(0.05)

command_images = get_basic_control_images()

'''
#default shell

time.sleep(5)

last_keys = []

for t in range(30 * 60 * 100):
    now_screen = get_music_screen_pixel()
    matches = match_command(now_screen, command_images)
    keys = match_to_list(matches)

    if (keys != last_keys):
        last_keys = keys

        for key in keys:
            if key is "a":
                key_press(gui.KEY_A, gui.KEY_SCAN_A)
            if key is "w":
                key_press(gui.KEY_W, gui.KEY_SCAN_W)
            if key is "d":
                key_press(gui.KEY_D, gui.KEY_SCAN_D)
            if key is "s":
                key_press(gui.KEY_S, gui.KEY_SCAN_S)

    print(keys)
'''
'''
# run one time
now_screen = get_music_screen_pixel()
matches = match_command(now_screen, command_images)
keys = match_to_list(matches)

print("".join(keys))
'''

# run in file connect

last_keys = []
connect_file_path = os.sep.join([os.path.expanduser("~lewis"), "Desktop", "code", "denc", "logs.txt"]);

while 1:
    now_screen = get_music_screen_pixel()
    matches = match_command(now_screen, command_images)
    keys = match_to_list(matches)

    if (keys != last_keys):
        content = "".join(keys)
        connect_file = open(connect_file_path, "w")
        connect_file.write(content)
        connect_file.close()
