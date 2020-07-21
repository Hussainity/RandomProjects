'''
Usage:
You'll need to pip install pyautogui, PIL, numpy, google_images_search, and keyboard
Just execute 'python AutoDraw.py'
Type in what you want to draw
Go to a painting program, ready your drawing tool, and press your shortcut (defuault is alt+x)
'''
import pyautogui as pag
import PIL
from PIL import Image
import numpy as np
from google_images_search import GoogleImagesSearch
import keyboard

query = input("What should we draw? ")

#######################################################

# User Specifc Settings

# Reference: https://pypi.org/project/Google-Images-Search/
cx = '016628267995734866728:ysx7l9q2hem' # you can use my image search engine
key = 'get a google developer key' # make sure the api for Custom Image Search is activated

# Where image files will be stored/read
path = 'wherever\you\want'

##########################################################

pag.PAUSE = 0.005 # time in seconds between each click

_search_params = {'q' : query + 'black and white', 'safe' : 'medium', 'fileType' : 'jpg|png', 'imgType' : 'clipart'}

pixel_dim = 2 # based on thickness of pen on screen

USELINES = True # draw lines instead of pixels - faster

n = 100 # image width (maintains aspect ratio)

shortcut = 'alt+x' # hotkey to start drawing

###########################################################

gis = GoogleImagesSearch(key, cx)

gis.search(search_params=_search_params, path_to_dir=path)

downloaded = gis.results()[0]._path

image = Image.open(downloaded).convert('RGB')
image = image.resize(size=(n+1, int(n * image.size[1] / image.size[0])))
image = PIL.ImageOps.mirror(image)

try:
    original = np.asarray(image)[:,:,0]
except IndexError:
    original = np.asarray(image)

data = original.copy()
data = np.rot90(data)

for ix,iy in np.ndindex(data.shape):
    if data[ix,iy] >= 255/2:
        data[ix,iy] = 0
    else:
        data[ix,iy] = 1

if (USELINES):
    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            if(data[row, col] == 1):
                count = 1
                while(row + count < data.shape[0]):
                    if (data[row + count, col] == 1):
                        data[row + count, col] = 0
                        count += 1
                    else:
                        break # look no one likes long while loop conditions ok
                data[row, col] = count


def on_triggered():
    start_x , start_y = pag.position()

    for row in range(data.shape[0]):
        for col in range(data.shape[1]):
            if data[row,col] == 1:
                pag.click(start_x + row*pixel_dim, start_y + col*pixel_dim)
            elif data[row, col] > 1:
                pag.moveTo(start_x + row*pixel_dim, start_y + col*pixel_dim)
                pag.dragTo(start_x + row*pixel_dim + pixel_dim*data[row,col], start_y + col*pixel_dim, button='left')

keyboard.add_hotkey(shortcut, on_triggered)
keyboard.wait('esc')
