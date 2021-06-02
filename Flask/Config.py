from builtins import str
from gpuinfo.nvidia import get_gpus
from collections import OrderedDict
from util.util import available_cams, DIR, cam_dimension
from util.util import DIR_DATA
import json
import natsort
import numpy as np
import multiprocessing
import threading
import time
import cv2
import os

global bool
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
        global_mask_file = DIR + "/data/" + str(self.index) + ".json"
        mask_dim = cam_dimension
        mask = np.zeros(mask_dim, dtype=np.uint8)

        with open(global_mask_file) as f:
            data = json.load(f)

        pts = []
        for key in data:
            regions = data.get(key).get('regions')

            for region in regions:
                if region.get('region_attributes').get('Object') == 'Mask':
                    xList = region.get('shape_attributes').get('all_points_x')
                    yList = region.get('shape_attributes').get('all_points_y')

                    for i in range(len(xList)):
                        pt = (xList[i], yList[i])
                        pts.append(pt)

                    pts = np.array([pts], dtype=np.int32)
                    pts = np.array([pts], dtype=np.int32)
                    cv2.fillPoly(mask, pts, (255, 255, 255))

        self.globalMaskPoints = pts
        self.globalMaskImage = mask

    def generate_parking_spots(self):
        parking_spot_file = DIR + "/data/" + str(self.index) + ".json"
        print("Reading : ", parking_spot_file)

        with open(parking_spot_file) as f:
            data = json.load(f)

        parking_spots = {}
        isOccupied = {}
        for key in data:
            regions = data.get(key).get('regions')

            for region in regions:
                if not region.get('region_attributes').get('Object') == 'Mask':
                    parking_spot_id = region.get('region_attributes').get('Object')
                    if "\n" in parking_spot_id:
                        parking_spot_id = parking_spot_id.replace("\n", "")
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
        self.parking_spots = OrderedDict(natsort.natsorted(self.parking_spots.items()))
        self.isSpotOccupied = OrderedDict(natsort.natsorted(self.isSpotOccupied.items()))


class ConfigServer():
    def __init__(self):
        self.GPU_Devices = []
        self.Listed_Cams = {}
        self.Active_Cams = {}
        self.isCamUp = False

    def configure(self):
        for key in available_cams:
            cam = Cam(key, available_cams.get(key))
            cam.generate_global_mask()
            cam.generate_parking_spots()
            self.Listed_Cams[key] = cam

            ip = available_cams.get(key)
            ip = (ip.split(":554")[0]).split("rtsp://")[1]
            self.Active_Cams[key] = (False, str(ip))

        for gpu in get_gpus():
            dict = gpu.__dict__
            mcs = gpu.get_max_clock_speeds()
            cs = gpu.get_clock_speeds()
            mem = gpu.get_memory_details()

            dev = GPU(dict.get('index'),
                      dict.get('name'),
                      dict.get('total_memory'),
                      mem.get('used_memory'),
                      mem.get('free_memory'))
            self.GPU_Devices.append(dev)

    def save_result(self):
        dict = {}
        for key in self.Listed_Cams:
            cam = self.Listed_Cams.get(key)
            dict[cam.index] = cam.isSpotOccupied
        with open(DIR_DATA + 'result.json', 'w') as json_file:
            json.dump(dict, json_file)

    def clean_jsons(self):
        if os.path.exists(DIR_DATA + 'result.json'):
            os.remove(DIR_DATA + 'result.json')
        if os.path.exists(DIR_DATA + 'activeCams.json'):
            os.remove(DIR_DATA + 'activeCams.json')

    def save_active_cams(self):
        with open(DIR_DATA + 'activeCams.json', 'w') as json_file:
            json.dump(self.Active_Cams, json_file)


def camStatusThread(key, stream_ip, dict, mutex):
    cap = cv2.VideoCapture(stream_ip)
    ret, frame = cap.read()
    if ret:
        mutex.acquire()
        dict[key] = True
        mutex.release()


def isCameraActive(key, config):
    cam = config.Listed_Cams.get(key)
    stream_ip = cam.cam_ip

    manager = multiprocessing.Manager()
    mutex = manager.Lock()
    dict = manager.dict()
    dict[key] = False

    process = multiprocessing.Process(target=camStatusThread, args=(key, stream_ip, dict, mutex,))
    process.start()

    time.sleep(8)
    process.terminate()

    print("Availability : ", dict)
    if dict[key]:
        IP = config.Active_Cams[key][1]
        config.Active_Cams[key] = (dict[key], IP)

    print(config.Active_Cams)
    return dict[key]