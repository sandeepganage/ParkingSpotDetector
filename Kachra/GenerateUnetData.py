import json
import numpy as np
import cv2


def generateUnetLabel():
    json_path = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/U_Net_Data/Annotations/combined.json"
    rgb_path = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/U_Net_Data/RGB/"
    lbl_out_path = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/U_Net_Data/Label/"
    ROI_out_path = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/U_Net_Data/ROI/"

    with open(json_path) as f:
        data = json.load(f)

    for key in data:
        image_name = key.split('.png')[0] + '.png'
        src_image = cv2.imread(rgb_path + image_name)
        mask = np.zeros(src_image.shape, dtype=np.uint8)

        value = data.get(key)
        regions = value.get('regions')

        for region in regions:
            xList = region.get('shape_attributes').get('all_points_x')
            yList = region.get('shape_attributes').get('all_points_y')

            pts = []
            for i in range(len(xList)):
                pt = (xList[i], yList[i])
                pts.append(pt)

            pts = np.array([pts], dtype=np.int32)
            cv2.fillPoly(mask, pts, (255, 255, 255))

        mask_roi = mask.copy()
        mask_roi[mask > 0] = 1
        cv2.imwrite(lbl_out_path + image_name, mask)
        cv2.imwrite(ROI_out_path + image_name, mask_roi)





        print()


generateUnetLabel()