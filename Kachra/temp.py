import cv2
import numpy as np
import math
from wrapt_timeout_decorator import *
from time import sleep

def AndOperationWithMask():
    img1 = "D:/DataOnly/ParkingManagement/Cam1/Masks/temp/01_20210309_180100.bmp"
    img2 = "D:/DataOnly/ParkingManagement/Cam1/Masks/temp/mask.png"

    img1 = cv2.imread(img1, cv2.IMREAD_COLOR)
    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)

    # img1 = img1.astype(np.uint8)
    # img2 = img2.astype(np.uint8)
    img1[img2 == 0] = 0

    cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/Masks/temp/mask_out.png", img1)


def GenerateTiles():
    img1 = "D:/DataOnly/ParkingManagement/Cam1/Masks/temp/mask_out.png"
    img1 = cv2.imread(img1)

    width = img1.shape[1]
    height = img1.shape[0]

    tile_Size = 768

    tiles_Across = 0
    tiles_Down = 0

    if width % tile_Size == 0:
        tiles_Across = math.trunc(width / tile_Size)
    else:
        tiles_Across = math.trunc(width / tile_Size) + 1

    if height % tile_Size == 0:
        tiles_Down = math.trunc(height / tile_Size)
    else:
        tiles_Down = math.trunc(height / tile_Size) + 1

    startx = 0
    starty = 0
    endx = 0
    endy = 0

    for ii in range(tiles_Down):
        for jj in range(tiles_Across):
            tile_name =  ii * tiles_Across + jj

            startx = jj * tile_Size
            starty = ii * tile_Size

            if startx + tile_Size > width:
                diff = width - startx
                diff = tile_Size - diff
                startx = startx - diff

            if starty + tile_Size > height:
                diff = height - starty
                diff = tile_Size - diff
                starty = starty - diff

            buffer = img1[starty : starty + tile_Size, startx : startx + tile_Size, :]
            cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/Masks/temp/"+str(tile_name)+".png", buffer)


def cyclic_learning_rates():
    for epoch in range(100):
        b = 0.2 * epoch
        lr = 0.00101 + 0.001 * np.cos(b + np.cos(b + np.cos(b + np.cos(b + np.cos(b + np.cos(b + np.cos(b)))))))
        print(epoch," : ", lr)


def getTimeDifference():
    import time
    start = time.time()

    time.sleep(10)  # or do something more productive

    done = time.time()
    elapsed = done - start
    print(elapsed)


def getDayOrNightTime():
    import time
    localtime = time.localtime()
    print(localtime)
    if localtime.tm_hour > 18:
        print("Its Night!")
    elif localtime.tm_hour < 6:
            print("Its Night!")
    else:
        print("Its Day!")



getDayOrNightTime()
# getTimeDifference()