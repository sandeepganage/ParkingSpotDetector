from jsonmerge import merge
import json
import random
import os
import shutil


def merge_JSON():
    file1 = "D:\DataOnly\ParkingManagement\TrainingData\Cam_1_2\cam1_drive_training_Data/out3.json"
    file2 = "D:\DataOnly\ParkingManagement\TrainingData\Cam_1_2\cam2_V_Parking/via_project_28Mar2021_16h10m_json.json"
    out = "D:\DataOnly\ParkingManagement\TrainingData\Cam_1_2\cam1_drive_training_Data/out.json"

    with open(file1) as f1:
        data1 = json.load(f1)

    with open(file2) as f2:
        data2 = json.load(f2)

    result = merge(data1, data2)

    with open(out, 'w') as outfile:
        json.dump(result, outfile)
    print()


def separate_train_test_JSON():
    split_ratio = 25

    file_extension = ".png"

    file = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Combined_Data_Annotations/Combined_Formatted/Annotations/combined.json"
    train_out = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Separated_Data_Annotations/Annotations/train.json"
    test_out = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Separated_Data_Annotations/Annotations/test.json"

    with open(file) as f:
        dict = json.load(f)

    total_elements = len(dict)
    test_size = int(total_elements / 100 * split_ratio)

    randomlist = random.sample(range(0, total_elements - 1), test_size)

    train_data = dict.copy()
    test_data = dict.copy()

    count = 0
    for key in dict:
        if count in randomlist:
            train_data.pop(key)
        count += 1

    for key in train_data:
        test_data.pop(key)

    with open(train_out, 'w') as outfile:
        json.dump(train_data, outfile)

    with open(test_out, 'w') as outfile:
        json.dump(test_data, outfile)

    print()


def separate_train_test_imagesFiles():
    inp_rgb = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Combined_Data_Annotations/Combined_Formatted/RGB/"
    out_train = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Separated_Data_Annotations/RGB/train/"
    out_test = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Separated_Data_Annotations/RGB/val/"

    inp_train_json = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Separated_Data_Annotations/Annotations/train.json"
    inp_test_json = "D:/DataOnly/ParkingManagement/TrainingData/Cam_1_2/Separated_Data_Annotations/Annotations/val.json"

    with open(inp_train_json) as f_train:
        dict_train = json.load(f_train)

    with open(inp_test_json) as f_test:
        dict_test = json.load(f_test)

    for key in dict_train:
        image_name = key.split('.png')[0]
        src_image_path = inp_rgb + image_name + ".png"
        dst_image_path = out_train + image_name + ".png"
        shutil.copy(src_image_path, dst_image_path)

    for key in dict_test:
        image_name = key.split('.png')[0]
        src_image_path = inp_rgb + image_name + ".png"
        dst_image_path = out_test + image_name + ".png"
        shutil.copy(src_image_path, dst_image_path)

    print()


# separate_train_test_JSON()
separate_train_test_imagesFiles()
