import multiprocessing
import time
import cv2
from util.util import available_cams
from threading import Lock
from util.util import DIR_DATA, IMG_OUT_SAVE_PATH
import os


mutex = Lock()


def func(key, ip, cam_status, mutex):
    capture = cv2.VideoCapture(ip)
    ret, frame = capture.read()
    print("Available : ", ret)
    if ret:
        mutex.acquire()
        cam_status[key] = True
        mutex.release()


def main():
    manager = multiprocessing.Manager()
    mutex = manager.Lock()
    cam_status = manager.dict()

    for key in available_cams:
        cam_status[key] = False

    print(cam_status)
    running_processes = []
    for key in available_cams:
        ip = available_cams.get(key)
        process = multiprocessing.Process(target=func, args=(key, ip, cam_status, mutex,))
        process.start()
        running_processes.append(process)

    time.sleep(5)

    for process in running_processes:
        process.terminate()
    print("-----------------------------------------------------------------")
    print(cam_status)
    for key in cam_status:
        dir_path = IMG_OUT_SAVE_PATH + "cam" + str(key)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        isCamUP = cam_status.get(key)
        if isCamUP:
            ip = available_cams.get(key)
            capture = cv2.VideoCapture(ip)
            ret, image = capture.read()
            cv2.imwrite(dir_path + "/0_rgb.jpg", image)
        else:
            image = cv2.imread(DIR_DATA + "StreamNotAvailable.jpg")
            cv2.imwrite(dir_path + "/0_rgb.jpg", image)


if __name__ == '__main__':
    main()