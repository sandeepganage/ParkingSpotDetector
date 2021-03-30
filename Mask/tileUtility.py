import cv2
import numpy as np
import math
from util.util import *
import os, glob


def GenerateTiles2(img, camID, tile_size):
    width = cam_dimension.get(camID)[1]
    height = cam_dimension.get(camID)[0]

    temp = np.zeros((height, height * 2, 3), dtype=np.uint8)
    temp[:, :width, :] = img[:, :, :]

    tile_list = []
    tile1 = temp[:, :tile_size, :]
    tile2 = temp[:, tile_size:, :]

    tile_list.append(tile1)
    tile_list.append(tile2)
    return tile_list


def resize_Tiles(tile_list, new_dim = 1536):
    resize_tile_list = []
    for tile in tile_list:
        new_tile = np.zeros((new_dim, new_dim, 3), dtype=np.uint8)
        curr_dim = tile.shape[0]
        diff = new_dim - curr_dim

        offset = int(diff / 2)
        new_tile[offset:new_dim-offset, offset:new_dim-offset, :] = tile[:, :, :]
        resize_tile_list.append(tile)
    return resize_tile_list;


def GenerateTiles(img1, camID, tile_size, image_name):
    out_dir = "D:/DataOnly/ParkingManagement/Cam1/capture/DataSet_2_17th_March/tiles_768/"
    width = cam_dimension.get(camID)[1]
    height = cam_dimension.get(camID)[0]

    if width % tile_size == 0:
        tiles_Across = math.trunc(width / tile_size)
    else:
        tiles_Across = math.trunc(width / tile_size) + 1

    if height % tile_size == 0:
        tiles_Down = math.trunc(height / tile_size)
    else:
        tiles_Down = math.trunc(height / tile_size) + 1

    tile_list = []
    for ii in range(tiles_Down):
        for jj in range(tiles_Across):
            tile_name = ii * tiles_Across + jj

            startx = jj * tile_size
            starty = ii * tile_size

            if startx + tile_size > width:
                diff = width - startx
                diff = tile_size - diff
                startx = startx - diff

            if starty + tile_size > height:
                diff = height - starty
                diff = tile_size - diff
                starty = starty - diff

            buffer = img1[starty: starty + tile_size, startx: startx + tile_size, :]
            tile_list.append(buffer)
            cv2.imwrite(out_dir + image_name + "_" +str(tile_name)+".png", buffer)

    return tile_list


def stitch_tiles(mask_list, camID, tile_size):
    width = cam_dimension.get(camID)[1]
    height = cam_dimension.get(camID)[0]

    tile_list = []
    for mask in mask_list:
        tile = np.zeros((tile_size, tile_size), dtype=np.uint8)
        num_images_per_mask = mask.shape[2]
        for i in range(num_images_per_mask):
            mask0 = mask[:, :, i]
            tile[mask0 == True] = 255

        tile_list.append(tile)

    image = np.zeros((height, height*2), dtype=np.uint8)

    image[:, :tile_size] = tile_list[0][:, :]
    image[:, tile_size:] = tile_list[1][:, :]
    out = image[:, :width]
    return out


def gen():
    inp = "D:/DataOnly/ParkingManagement/Cam1/capture/DataSet_2_17th_March/Masked/"
    images = sorted(glob.glob(inp + "*.bmp"))

    for image in images:
        image_name = os.path.basename(image)
        img = cv2.imread(image)
        GenerateTiles(img, 1, 768, image_name)


# gen()