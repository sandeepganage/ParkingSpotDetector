from mrcnn.config import Config
from Flask.Config import ConfigServer, isCameraActive, activateClient
from mrcnn import model as modellib
from keras.preprocessing.image import img_to_array
from IPOperations.IPOperations import cam1_IP, getSpotResults, getSpotResultsAllFalse, blurr_outside_roi
from Mask.tileUtility import *
from util.util import DIR_DATA, IMG_OUT_SAVE_PATH
import cv2
import time

# global config

StaticDebugMode = False
saveDebugRes = True
global clientProcess
global isClientRunning


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
    global clientProcess
    global isClientRunning
    isClientRunning = False
    start_time = 0
    end_time = 0

    config = ConfigServer()
    config.configure()
    config.clean_jsons()
    config.save_result()

    dev = config.GPU_Devices[0]
    os.environ["CUDA_VISIBLE_DEVICES"] = str(dev.index)

    modelConfig = myMaskRCNNConfig()
    modelConfig.display()

    # Loading the model in the inference mode
    model_day = modellib.MaskRCNN(mode="inference", config=modelConfig, model_dir='./')
    model_night = modellib.MaskRCNN(mode="inference", config=modelConfig, model_dir='./')

    # loading the trained weights o the custom dataset
    MODEL_PATH_DAY = DIR_DATA + available_model.get(1)
    MODEL_PATH_NIGHT = DIR_DATA + available_model.get(2)

    model_day.load_weights(MODEL_PATH_DAY, by_name=True)
    model_night.load_weights(MODEL_PATH_NIGHT, by_name=True)

    while True:
        if not isClientRunning:
            print("Staring client")
            clientProcess = activateClient()
            start_time = time.time()
            isClientRunning = True

        for key in config.Listed_Cams:
            dir_path = IMG_OUT_SAVE_PATH + str(key)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            cam = config.Listed_Cams.get(key)
            isCamUP = isCameraActive(key, config)
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
                        image = DIR_DATA + str(key) + "Ref.png"
                        image = cv2.imread(image)

                    else:
                        image = image.astype(np.uint8)
                        cv2.polylines(image, cam.globalMaskPoints, True, (0, 255, 0), thickness=3)

                        blurred_Non_roi = blurr_outside_roi(image, cam.globalMaskImage)
                        cv2.imwrite(dir_path + "/0_rgb.jpg", blurred_Non_roi)

                        image[cam.globalMaskImage == 0] = 0

                        tiles = GenerateTiles2(image, cam.index, 1296)
                        tiles = resize_Tiles(tiles)

                        mask_list = []
                        for tile in tiles:
                            img = img_to_array(tile)
                            if isDayTime():
                                results = model_day.detect([img], verbose=1)
                            else:
                                results = model_night.detect([img], verbose=1)
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

            config.save_result()
            config.save_active_cams()

        end_time = time.time()
        elapsed = end_time - start_time
        # print("Start_time : ", start_time, "\tEnd_time : ", end_time, "\tElapsed_Time : ", elapsed)
        if elapsed > 300:
            start_time = 0
            print("TimeOut. Terminating Client Code..")
            clientProcess.terminate()
            isClientRunning = False

        if not clientProcess.is_alive():
            start_time = 0
            print("Network disconnected. Terminating Client Code..")
            isClientRunning = False


def isDayTime():
    localtime = time.localtime()
    # print(localtime)
    if localtime.tm_hour > 18:
        # print("Its Night!")
        return False
    elif localtime.tm_hour < 6:
            # print("Its Night!")
            return False
    else:
        # print("Its Day!")
        return True


if __name__ == '__main__':
    execute()
