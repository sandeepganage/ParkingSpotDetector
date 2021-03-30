import numpy as np
import cv2
from util.util import decision_threshold

class IPOperations:
    def __init__(self, ):
        self.name = "obj"

    def fine_tune_dl(self, mask, input):
        # img = cv2.imread("D:/DataOnly/ParkingManagement/Cam1/training_data2/fine_tune_dl/out.png")
        img = cv2.bitwise_not(input)
        mask_image = mask.copy()
        mask_image = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
        img = mask_image & img
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/training_data2/fine_tune_dl/1.png", img)
        gray = self.fill_hole(img)
        # cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/training_data2/fine_tune_dl/2.png", gray)

        kernel = np.ones((10, 10), np.uint8)
        im_erode = cv2.morphologyEx(gray, cv2.MORPH_ERODE, kernel)
        # cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/training_data2/fine_tune_dl/3.png", im_erode)

        kernel = np.ones((10, 10), np.uint8)
        im_open = cv2.morphologyEx(im_erode, cv2.MORPH_OPEN, kernel)
        # cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/training_data2/fine_tune_dl/4.png", im_open)

        img2 = self.area_open(im_open, 1000)
        # cv2.imwrite("D:/DataOnly/ParkingManagement/Cam1/training_data2/fine_tune_dl/5.png", img2)
        return img2

    def area_open(self, mask, threshold):
        # find all your connected components (white blobs in your image)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
        # connectedComponentswithStats yields every seperated component with information on each of them, such as size
        # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
        sizes = stats[1:, -1];
        nb_components = nb_components - 1

        # minimum size of particles we want to keep (number of pixels)
        # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
        min_size = threshold

        # your answer image
        img2 = np.zeros((output.shape))
        # for every component in the image, you keep it only if it's above min_size
        for i in range(0, nb_components):
            if sizes[i] >= min_size:
                img2[output == i + 1] = 255

        return img2

    def area_open_invert(self, mask, threshold):
        # find all your connected components (white blobs in your image)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
        # connectedComponentswithStats yields every seperated component with information on each of them, such as size
        # the following part is just taking out the background which is also considered a component, but most of the time we don't want that.
        sizes = stats[1:, -1];
        nb_components = nb_components - 1

        # minimum size of particles we want to keep (number of pixels)
        # here, it's a fixed value, but you can set it as you want, eg the mean of the sizes or whatever
        max_size = threshold

        # your answer image
        img2 = np.zeros((output.shape))
        # for every component in the image, you keep it only if it's below max_size
        for i in range(0, nb_components):
            if sizes[i] >= max_size:
                img2[output == i + 1] = 255

        return img2

    def fill_hole(self, im_in):
        im_floodfill = im_in.copy()

        # Mask used to flood filling.
        # Notice the size needs to be 2 pixels than the image.
        h, w = im_in.shape[:2]
        mask = np.zeros((h + 2, w + 2), np.uint8)

        # Floodfill from point (0, 0)
        cv2.floodFill(im_floodfill, mask, (0, 0), 255);

        # Invert floodfilled image
        im_floodfill_inv = cv2.bitwise_not(im_floodfill)

        # Combine the two images to get the foreground.
        im_out = im_in | im_floodfill_inv

        return im_out

    def __del__(self):
        return True


def sampleMeanStd(img):
    img = img.astype("float32")

    b_ch = np.mean(img[:, :, 0])
    g_ch = np.mean(img[:, :, 1])
    r_ch = np.mean(img[:, :, 2])

    # Individual channel-wise mean subtraction
    img -= np.array((b_ch, g_ch, r_ch))

    b_ch = np.std(img[:, :, 0])
    g_ch = np.std(img[:, :, 1])
    r_ch = np.std(img[:, :, 2])

    img /= np.array((b_ch, g_ch, r_ch))
    return img


def cam1_IP(inpRGB, prediction):
    save_result = False
    out_dir = "D:/DataOnly/ParkingManagement/Cam1/debug/"

    if save_result:
        cv2.imwrite(out_dir + "1.png", inpRGB)
        cv2.imwrite(out_dir + "2.png", prediction)
    ip_ops = IPOperations()
    # prediction = IPOperations.area_open(prediction)
    mask_cam2_partA = "D:/DataOnly/ParkingManagement/Cam2/training_data/mask_cam2_partA.png"
    mask_cam2_partA = cv2.imread(mask_cam2_partA, cv2.IMREAD_GRAYSCALE)
    if save_result:
        cv2.imwrite(out_dir + "3.png", mask_cam2_partA)

    prediction = prediction.astype(np.uint8)
    prediction = 255 - prediction
    if save_result:
        cv2.imwrite(out_dir + "4.png", prediction)

    # prediction = cv2.cvtColor(prediction, cv2.COLOR_BGR2GRAY)
    prediction = prediction.astype(np.uint8)
    prediction = prediction & mask_cam2_partA
    if save_result:
        cv2.imwrite(out_dir + "5.png", prediction)

    kernel = np.ones((10, 10), np.uint8)
    prediction = cv2.morphologyEx(prediction, cv2.MORPH_OPEN, kernel)
    if save_result:
        cv2.imwrite(out_dir + "6.png", prediction)

    kernel = np.ones((10, 10), np.uint8)
    prediction = cv2.morphologyEx(prediction, cv2.MORPH_OPEN, kernel, iterations=5)
    if save_result:
        cv2.imwrite(out_dir + "7.png", prediction)

    prediction = ip_ops.area_open(prediction, 2000)
    if save_result:
        cv2.imwrite(out_dir + "8.png", prediction)

    inpRGB = inpRGB.astype(np.uint8)
    gray = cv2.cvtColor(inpRGB, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    if save_result:
        cv2.imwrite(out_dir + "9_otsu.png", thresh)

    kernel = np.ones((8, 8), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    if save_result:
        cv2.imwrite(out_dir + "10_CLOSE.png", thresh)

    kernel = np.ones((2, 2), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    if save_result:
        cv2.imwrite(out_dir + "11_Dilate.png", thresh)

    thresh = 255 - thresh
    if save_result:
        cv2.imwrite(out_dir + "12_Invert.png", thresh)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_ERODE, kernel)
    if save_result:
        cv2.imwrite(out_dir + "13_Open.png", thresh)

    prediction = prediction.astype(np.uint8)
    out = prediction & thresh
    if save_result:
        cv2.imwrite(out_dir + "14_Open.png", out)

    # print("Done!")
    return out


def cam1_IP(inpRGB, dl_out):
    out_dir = "D:/DataOnly/ParkingManagement/Cam1/debug/"
    save_result = False

    if save_result:
        cv2.imwrite(out_dir + "0_DL.png", dl_out)

    inpRGB = inpRGB.astype(np.uint8)
    gray = cv2.cvtColor(inpRGB, cv2.COLOR_BGR2GRAY)

    thresh1 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 5)
    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 199, 5)
    if save_result:
        cv2.imwrite(out_dir + "1.2_AdaThreshold.png", thresh2)
        cv2.imwrite(out_dir + "1.1_AdaThreshold.png", thresh1)

    inpRGB = inpRGB.astype(np.uint8)
    inpRGB = cv2.GaussianBlur(inpRGB, (5, 5), 1.4)
    gray = cv2.cvtColor(inpRGB, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    if save_result:
        cv2.imwrite(out_dir + "2_otsu.png", thresh)

    kernel = np.ones((3, 3), np.uint8)
    dl_out = cv2.morphologyEx(dl_out, cv2.MORPH_ERODE, kernel)
    if save_result:
        cv2.imwrite(out_dir + "3_ErodeDL.png", dl_out)

    thresh2 = thresh2.astype(np.uint8)
    dl_out = dl_out.astype(np.uint8)
    out = thresh2 & dl_out
    if save_result:
        cv2.imwrite(out_dir + "4_AND.png", out)

    kernel = np.ones((3, 3), np.uint8)
    out = cv2.morphologyEx(out, cv2.MORPH_ERODE, kernel)
    if save_result:
        cv2.imwrite(out_dir + "5_Final.png", out)
    return out


def getSpotResults(IP_Out, cam):
    for key in cam.parking_spots:
        pts = cam.parking_spots[key]
        mask = np.zeros(IP_Out.shape, dtype=np.uint8)
        cv2.fillPoly(mask, pts, 255)
        img = IP_Out.copy()
        img[mask == 0] = 0
        spot_dl_count = np.count_nonzero(img)
        mask_area = np.count_nonzero(mask)
        occupied_percent = (spot_dl_count / mask_area) * 100
        # print("Area : ", mask_area, "    occupied_pixels : ", spot_dl_count, "    occupied_percent : ", occupied_percent)
        if occupied_percent > decision_threshold:
            cam.isSpotOccupied[key] = True          #Parking Spot Occupied
        else:
            cam.isSpotOccupied[key] = False         #Parking Spot Not Occupied

def fun12():
    deep_out = cv2.imread("D:/DataOnly/ParkingManagement/Cam1/debug/DL.png", cv2.IMREAD_GRAYSCALE)
    img = cv2.imread("D:/DataOnly/ParkingManagement/Cam1/debug/RGB.png")
    # img = cv2.imread("D:/DataOnly\ParkingManagement/Cam1/testing/01_20210315_134832.bmp")
    # img = cv2.imread("D:/DataOnly\ParkingManagement/Cam1/debug/input/0311_152948.bmp")
    cam1_IP(img, deep_out)

# fun12()
# fun12()
# rgb = "D://DataOnly//ParkingManagement//Cam1//View2//debug//IP_5//0.png"
# rgb = cv2.imread(rgb)
# cam1_IP2(rgb)
