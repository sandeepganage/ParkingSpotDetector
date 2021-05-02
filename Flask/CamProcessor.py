import multiprocessing
import time
from threading import Lock
from mrcnn.config import Config
from Flask.Config import ConfigServer
from mrcnn import model as modellib
from keras.preprocessing.image import img_to_array
from IPOperations.IPOperations import cam1_IP, getSpotResults, getSpotResultsAllFalse
from Mask.tileUtility import *
from util.util import DIR_DATA, IMG_OUT_SAVE_PATH
import cv2
import json

global config

StaticDebugMode = False
saveDebugRes = True


class myMaskRCNNConfig(Config):
    # give the configuration a recognizable name
    NAME = "MaskRCNN_config"

    # set the number of GPUs to use along with the number of images
    # per GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # number of classes (we would normally add +1 for the background)
    # kangaroo + BG
    NUM_CLASSES = 1 + 1

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 131

    # Learning rate
    LEARNING_RATE = 0.006

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9

    # setting Max ground truth instances
    MAX_GT_INSTANCES = 10

    IMAGE_MAX_DIM = 1536


def execute(working_cams):
    global config
    config = ConfigServer()
    config.configure()
    save_result()

    dev = config.GPU_Devices[0]
    os.environ["CUDA_VISIBLE_DEVICES"] = str(dev.index)

    modelConfig = myMaskRCNNConfig()
    modelConfig.display()

    # Loading the model in the inference mode
    model = modellib.MaskRCNN(mode="inference", config=modelConfig, model_dir='./')

    # loading the trained weights o the custom dataset
    MODEL_PATH = DIR_DATA + available_model.get(1)
    model.load_weights(MODEL_PATH, by_name=True)

    while True:
        for key in config.Active_Cams:
            dir_path = IMG_OUT_SAVE_PATH + "cam" + str(key)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            cam = config.Active_Cams.get(key)

            isCamUP = working_cams.get(key)
            if isCamUP:
                capture = cv2.VideoCapture(cam.cam_ip)
                ret, image = capture.read()
                if not ret:
                    image = cv2.imread(DIR_DATA + "StreamNotAvailable.jpg")
                    cv2.imwrite(dir_path + "/0_rgb.jpg", image)
                    getSpotResultsAllFalse(cam)
                    print("Streaming Not for working for Cam : %d", key)
                else:
                    if StaticDebugMode:
                        image = DIR_DATA + str(key)+"Ref.png"
                        image = cv2.imread(image)

                    else:
                        image = image.astype(np.uint8)
                        cv2.polylines(image, cam.globalMaskPoints, True, (0, 255, 0), thickness=3)
                        cv2.imwrite(dir_path + "/0_rgb.jpg", image)

                        image[cam.globalMaskImage == 0] = 0

                        tiles = GenerateTiles2(image, cam.index, 1296)
                        tiles = resize_Tiles(tiles)

                        mask_list = []
                        for tile in tiles:
                            img = img_to_array(tile)
                            results = model.detect([img], verbose=1)
                            r = results[0]
                            # visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], r['scores'], title="Predictions")
                            masks = r['masks']
                            mask_list.append(masks)
                            print()
                        dlOut = stitch_tiles(mask_list, cam.index, 1296)
                        ipOut = cam1_IP(image, dlOut, key)
                        getSpotResults(ipOut, cam)
                        # config.Active_Cams[key] = cam

                        if saveDebugRes:
                            cv2.imwrite(dir_path + "/1_rgb.jpg", image)
                            cv2.imwrite(dir_path + "/2_DL_Out.jpg", dlOut)
                            cv2.imwrite(dir_path + "/3_IP_Out.jpg", ipOut)

            else:
                image = cv2.imread(DIR_DATA + "StreamNotAvailable.jpg")
                cv2.imwrite(dir_path + "/0_rgb.jpg", image)
                getSpotResultsAllFalse(cam)
                print("Streaming Not for working for Cam : %d", key)

            save_result()


def save_result():
    global config
    dict = {}
    for key in config.Active_Cams:
        cam = config.Active_Cams.get(key)
        cam_id = cam.index
        dict[cam_id] = cam.isSpotOccupied
    with open(DIR_DATA + 'result.json', 'w') as json_file:
        json.dump(dict, json_file)


mutex = Lock()


def func(key, ip, cam_status, mutex):
    capture = cv2.VideoCapture(ip)
    ret, frame = capture.read()
    print("Available : ", ret)
    if ret:
        mutex.acquire()
        cam_status[key] = True
        mutex.release()


def get_working_cams():
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

    time.sleep(10)

    for process in running_processes:
        process.terminate()
    print("-----------------------------------------------------------------")
    print(cam_status)
    return cam_status


if __name__ == '__main__':
    working_cams = get_working_cams()
    with open(DIR_DATA + 'activeCams.json', 'w') as json_file:
        json.dump(working_cams.copy(), json_file)

    execute(working_cams)
