import json
#from gpuinfo.nvidia import get_gpus
import os
import Networks
from util.util import userID, available_cams, password, DIR, cam_dimension
import numpy as np
import cv2


class GPU():
    def __init__(self, index, name, total_memory, used_memory, free_memory):
        self.index = index
        self.name = name
        self.total_memory = total_memory
        self.used_memory = used_memory
        self.free_memory = free_memory
        self.isOccupied = False

    def update_info(self):
        gpu = get_gpus()[self.index]
        dict = gpu.__dict__
        mem = gpu.get_memory_details()
        self.total_memory = dict.get('total_memory')
        self.used_memory = mem.get('used_memory')
        self.free_memory = mem.get('free_memory')

    def show_info(self):
        print("Name: ", self.name)
        print("Index: ", self.index)
        print("Total Memory: ", self.total_memory)
        print("Used Memory: ", self.used_memory)
        print("Free Memory: ", self.free_memory)


class Cam():
    def __init__(self, index, cam_ip):
        self.index = index
        self.cam_ip = cam_ip
        self.globalMaskImage = None
        self.globalMaskPoints = None
        self.parking_spots = None
        self.isSpotOccupied = None
        self.parking_results = None
        self.last_dl_output = None
        self.last_masked_rgb_input = None
        self.last_processed_output = None

    def generate_global_mask(self):
        global_mask_file = DIR + "/data/" + str(self.index) + "_GlobalMask.json"
        mask_dim = cam_dimension.get(self.index)
        mask = np.zeros(mask_dim, dtype=np.uint8)

        with open(global_mask_file) as f:
            data = json.load(f)

        for key in data:
            regions = data.get(key).get('regions')

            for region in regions:
                xList = region.get('shape_attributes').get('all_points_x')
                yList = region.get('shape_attributes').get('all_points_y')

                pts = []
                for i in range(len(xList)):
                    pt = (xList[i], yList[i])
                    pts.append(pt)

                pts = np.array([pts], dtype=np.int32)
                pts = np.array([pts], dtype=np.int32)
                cv2.fillPoly(mask, pts, (255, 255, 255))

        self.globalMaskPoints = pts
        self.globalMaskImage = mask

    def generate_parking_spots(self):
        parking_spot_file = DIR + "/data/" + str(self.index) + "_ParkingSpots.json"

        with open(parking_spot_file) as f:
            data = json.load(f)

        parking_spots = {}
        isOccupied = {}
        for key in data:
            regions = data.get(key).get('regions')

            for region in regions:
                parking_spot_id = region.get('region_attributes').get('Object')
                xList = region.get('shape_attributes').get('all_points_x')
                yList = region.get('shape_attributes').get('all_points_y')

                pts = []
                for i in range(len(xList)):
                    pt = (xList[i], yList[i])
                    pts.append(pt)
                pts = np.array([pts], dtype=np.int32)
                parking_spots[parking_spot_id] = pts
                isOccupied[parking_spot_id] = False

        self.parking_spots = parking_spots
        self.isSpotOccupied = isOccupied


class ConfigServer():
    def __init__(self):
        self.GPU_Devices = []
        self.Active_Cams = {}

    def configure(self):
        for key in available_cams:
            cam = Cam(key, available_cams.get(key))
            cam.generate_global_mask()
            cam.generate_parking_spots()
            self.Active_Cams[key] = cam

        # for gpu in get_gpus():
        #     dict = gpu.__dict__
        #     mcs = gpu.get_max_clock_speeds()
        #     cs = gpu.get_clock_speeds()
        #     mem = gpu.get_memory_details()
        #
        #     dev = GPU(dict.get('index'),
        #               dict.get('name'),
        #               dict.get('total_memory'),
        #               mem.get('used_memory'),
        #               mem.get('free_memory'))
        #     self.GPU_Devices.append(dev)