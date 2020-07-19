import time
import pyautogui as pag
import PIL
from PIL import Image
import numpy as np
from google_images_search import GoogleImagesSearch
import glob
import os

#######################################################

cx = '016628267995734866728:ysx7l9q2hem'
key = ''

path = 'C:\\Users\\hussa\\Documents\\PersonalProjects\\AutoDraw\\Images\\'

##########################################################

pag.PAUSE = 0.001

_search_params = {'q' : 'international space station clip art black and white', 'imgType' : 'clipart'}

pixel_dim = 3

###########################################################

gis = GoogleImagesSearch(key, cx)

gis.search(search_params=_search_params, path_to_dir=path)

list_of_files = glob.glob(path + '*')
latest_file = max(list_of_files, key=os.path.getctime)


image = Image.open(latest_file)
n = 150
image = image.resize(size=(n, int(n * image.size[1] / image.size[0])))
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

drawing = data.tolist()

time.sleep(3)

start_x , start_y = pag.position()

for x, row in enumerate(drawing):
    for y, e in enumerate(row):
        if e:
            pag.click(start_x + x*pixel_dim, start_y + y*pixel_dim)
