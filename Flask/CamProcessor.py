from mrcnn.config import Config
from Flask.Config import ConfigServer
from mrcnn import model as modellib
from keras.preprocessing.image import img_to_array
from IPOperations.IPOperations import cam1_IP, getSpotResults
from Mask.tileUtility import *
from util.util import DIR_DATA
import cv2
import json

global config

StaticMode = False
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


def execute():
    global config
    config = ConfigServer()
    config.configure()
    save_result()

    # dev = config.GPU_Devices[0]
    # os.environ["CUDA_VISIBLE_DEVICES"] = str(dev.index)

    modelConfig = myMaskRCNNConfig()
    modelConfig.display()

    # Loading the model in the inference mode
    model = modellib.MaskRCNN(mode="inference", config=modelConfig, model_dir='./')

    # loading the trained weights o the custom dataset
    MODEL_PATH = DIR_DATA + available_model.get(1)
    model.load_weights(MODEL_PATH, by_name=True)

    while True:
        for key in config.Active_Cams:
            cam = config.Active_Cams.get(key)
            cam_login = cam.cam_ip
            capture = cv2.VideoCapture(cam_login)
            if not capture.isOpened():
                print("Streaming for working for Cam : %d", key)
                # print()
            else:
                ret, image = capture.read()

                if StaticMode:
                    image = "C:/ParkingSpotDetector/data/"+str(key)+"Ref.png"
                    image = cv2.imread(image)

                if not ret:
                    print("Image capture failed for camera : ", key)

                else:
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
                    ipOut = cam1_IP(image, dlOut)
                    getSpotResults(ipOut, cam)
                    config.Active_Cams[key] = cam
                    save_result()
                    if saveDebugRes:
                        cv2.imwrite("D:/temp/cam"+str(key)+"/1_rgb.png",image)
                        cv2.imwrite("D:/temp/cam" + str(key) + "/2_DL_Out.png", dlOut)
                        cv2.imwrite("D:/temp/cam" + str(key) + "/3_IP_Out.png", ipOut)


def save_result():
    global config
    dict = {}
    for key in config.Active_Cams:
        cam = config.Active_Cams.get(key)
        cam_id = cam.index
        dict[cam_id] = cam.isSpotOccupied
    # json_object = json.dumps(dict)
    with open(DIR_DATA + 'result.json', 'w') as json_file:
        json.dump(dict, json_file)


if __name__ == '__main__':
    execute()
