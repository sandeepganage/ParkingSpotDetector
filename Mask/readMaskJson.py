import json
import os
import shutil
import glob
import cv2
import numpy as np


def read_edit_json():
    with open("D://DataOnly//ParkingManagement//Cam4//train_data//via_project_24Feb2021_12h11m_json.json") as f:
      data = json.load(f)

    # Output: {'name': 'Bob', 'languages': ['English', 'Fench']}
    data1 = data.copy()
    Dict = {}
    for key in data1.keys():
        if len(data.get(key).get('regions')) == 0:
            pass
        else:
            Dict[key] = data1.get(key)

    with open("D://DataOnly//ParkingManagement//Cam4//train_data//via_project_24Feb2021_12h11m_json2.json", 'w') as fp:
        json.dump(Dict, fp)

    print('done')


def move_images_from_json():
    inp_dir = "D:/DataOnly/ParkingManagement/MaskRCNN/src/"
    out_dir = "D:/DataOnly/ParkingManagement/MaskRCNN/dst/"

    json_path = "D:/DataOnly/ParkingManagement/MaskRCNN/via_project_24Feb2021_12h11m_json.json"

    with open(json_path) as f:
        data = json.load(f)

    for key in data.keys():
        filename = data.get(key).get('filename')
        shutil.move(inp_dir + filename, out_dir + filename)


def create_global_Mask():
    image_path = "D:/DataOnly/ParkingManagement/Cam1/capture/DataSet_2_17th_March/01_20210315_173307.bmp"
    src_image = cv2.imread(image_path)
    mask = np.zeros(src_image.shape, dtype=np.uint8)

    with open("D:/DataOnly/ParkingSpotDetector/data/1_GlobalMask.json") as f:
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

            print(pts)
            pts = np.array([pts], dtype=np.int32)
            cv2.fillPoly(mask, pts, (255, 255, 255))
            cv2.imwrite("D://DataOnly//ParkingManagement//Cam1//capture//DataSet_2_17th_March//mask.png", mask)
            # print("Done!")

    return mask


def getParkingSpots(camID):
    parkingSpotsJSONFile = None
    if camID == 1:
        parkingSpotsJSONFile = "A1_ParkingSpots.json"

    with open(parkingSpotsJSONFile) as f:
      data = json.load(f)

    parking_spots = []
    for key in data:
        regions = data.get(key).get('regions')

        for region in regions:
            xList = region.get('shape_attributes').get('all_points_x')
            yList = region.get('shape_attributes').get('all_points_y')

            pts = []
            for i in range(len(xList)):
                pt = (xList[i], yList[i])
                pts.append(pt)

            print(pts)
            pts = np.array([pts], dtype=np.int32)
            parking_spots.append(pts)
            # cv2.fillPoly(mask, pts, (255, 255, 255))

    return parking_spots


def AndOperation():
    mask_image = "D://DataOnly//ParkingManagement//Cam1//capture//DataSet_2_17th_March//mask.png"
    mask_image = cv2.imread(mask_image)
    images = sorted(glob.glob("D:/DataOnly/ParkingManagement/Cam1/capture/DataSet_2_17th_March/RGB/*.bmp"))
    out_dir = "D:/DataOnly/ParkingManagement/Cam1/capture/DataSet_2_17th_March/Masked/"

    for image in images:
        image_name = os.path.basename(image)
        img = cv2.imread(image)
        img[mask_image == 0] = 0

        cv2.imwrite(out_dir + image_name, img)





AndOperation()
# create_global_Mask()