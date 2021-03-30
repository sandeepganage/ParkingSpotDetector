from mrcnn.config import Config
from mrcnn import model as modellib
from mrcnn import visualize
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array


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


modelConfig = myMaskRCNNConfig()
modelConfig.display()

# Loading the model in the inference mode
model = modellib.MaskRCNN(mode="inference", config=modelConfig, model_dir='./')

# loading the trained weights o the custom dataset
model.load_weights("C:/Users/Sandeep/Downloads/mask_rcnn_containers_0117.h5", by_name=True)


img = load_img("D:/DataOnly/ParkingManagement/Cam1/Masks/temp/2.png")
img = img_to_array(img)

# detecting objects in the image
results = model.detect([img], verbose=1)

r = results[0]

visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'], r['scores'], title="Predictions")

print('Done!')