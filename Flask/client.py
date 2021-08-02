import cv2
import requests
import pyodbc
import time
import json
from datetime import datetime
import base64
import os
from util.util import IMG_OUT_SAVE_PATH, DIR_DATA
import urllib3
import numpy as np
urllib3.disable_warnings()

# "MyProjectConnection": "server=tcp:rit-dbsvr-01.database.windows.net;database=JNPT;User id=ritdbadmin@rit-dbsvr-01;password=Aez@3105.db"

server = 'tcp:azinwipresdb01.database.windows.net'
database = 'JNPT'
username = 'ritescdbsuser@azinwipresdb01'
password = 'ZU5ima5@BXS3mYlazXhSy'

# server = 'aaditechdb.database.windows.net'
# database = 'JNPT_QA'
# username = 'aaditechadmin'
# password = 'AadiTech@123'

# conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
# cursor = conn.cursor()
# conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=localhost\SQLEXPRESS; Database=ParkingAi; trusted_connection=YES;")


# IP = 'http://127.0.0.1'
# PORT = '5000'
# API = 'get_parking_results'
# API_CamStatus = 'get_active_cams'
global json_camStatus_path
global json_result_path
global cam_ref_images

json_camStatus_path = DIR_DATA + 'activeCams.json'
json_result_path = DIR_DATA + 'result.json'
cam_ref_images = {}


def storedb(key, isCamUP, camIP):
    CAM_IMG_PATH = str(IMG_OUT_SAVE_PATH) + str(key) + "/0_rgb.jpg"
    image = cv2.imread(CAM_IMG_PATH)
    print(CAM_IMG_PATH)
    scale_percent = 20  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    image_bytes = cv2.imencode('.jpg', resized)[1].tobytes()

    # cursor.execute(
    #     "UPDATE Parking_Image SET UpdateTime = getdate() , LatestImage = ?, IsLive = ? WHERE Camera = ?",
    #     image_bytes, isCamUP, str(key));
    # conn.commit();

    current_time = datetime.now()
    current_time = str(current_time)
    print("Camera Status for cam: ",key," : ",isCamUP)
    if isCamUP == "1":
        isCamUP = True
        # print("Camera Status for cam: ", key, " : ", isCamUP)
    else:
        isCamUP = False
        # print("Camera Status for cam: ", key, " : ", isCamUP)
    img_base64 = base64.b64encode(image_bytes).decode("utf8")
    payload_image = {"UpdateTime": current_time, "LatestImage": img_base64, "IsLive": isCamUP, "Camera": str(key), "IPAddress": str(camIP)}
    payload_json_image = json.dumps(payload_image)

    headers_image = {
        'Content-Type': 'application/json'
    }

    respo = requests.post("https://api.jnptparking.in/api/Parking/UpdateParkingImage", data=payload_json_image, headers=headers_image, verify=False)
    # respo = requests.post("http://122.186.213.190:8084/api/Parking/UpdateParkingImage", data=payload_json_image, headers=headers_image, verify=False)
    print(key, ": Image POST Status 1 : ",respo.text)


def generate_compare_masks():
    global json_camStatus_path
    global json_result_path
    global cam_ref_images

    while not os.path.exists(json_result_path):
        time.sleep(5)
        print("Result not ready yet! Waiting..")

    with open(json_result_path) as f:
        results = json.load(f)

    for key in results:
        f_metadata = DIR_DATA + str(key) + ".json"
        with open(f_metadata) as f:
            f_metadata = json.load(f)
        mask_pts = []
        for entry in f_metadata:
            regions = f_metadata.get(entry).get('regions')
            for region in regions:
                if region.get('region_attributes').get('Object') == 'Mask':
                    xList = region.get('shape_attributes').get('all_points_x')
                    yList = region.get('shape_attributes').get('all_points_y')

                    for i in range(len(xList)):
                        pt = (xList[i], yList[i])
                        mask_pts.append(pt)

        mask_pts = np.array([mask_pts], dtype=np.int32)
        cam_num = str(key).split("C")[1]

        ref_image = DIR_DATA + cam_num + "Ref.png"
        if not os.path.exists(ref_image):
            print("Reference Image for Cam",key,"is not present!")
            exit(1)
        else:
            ref_image = cv2.imread(ref_image, cv2.IMREAD_UNCHANGED)

            ref_image = ref_image.astype(np.uint8)
            cv2.polylines(ref_image, mask_pts, True, (0, 255, 0), thickness=3)
            cam_ref_images[key] = ref_image


def main():
    global json_camStatus_path
    global json_result_path
    global cam_ref_images
    # url = IP + ":" + PORT + "/" + API
    # url_camStatus = IP + ":" + PORT + "/" + API_CamStatus

    count = 0
    while True:
        # json_result = requests.post(url).json()
        # json_camStatus = requests.post(url_camStatus).json()
        while not os.path.exists(json_camStatus_path):
            time.sleep(5)
            print("Result not ready yet! Waiting..")

        while not os.path.exists(json_result_path):
            time.sleep(5)
            print("Result not ready yet! Waiting..")

        with open(json_result_path) as f:
            json_result = json.load(f)

        with open(json_camStatus_path) as f:
            json_camStatus = json.load(f)

        #print(json_result)
        if count == 2:
            print(count)
            count = 0

            for key in json_result:
                tuple = json_camStatus.get(key)
                isCamUP = tuple[0]
                camIP = tuple[1]

                if isCamUP:
                    isCamUP = "1"
                else:
                    isCamUP = "0"
                storedb(key, isCamUP, camIP)
                result = json_result.get(key)
                # print(json_result)
                # print("Updating Cam result :/ ",key)

                for spot_result in result:
                    pid = spot_result
                    p_value = result.get(spot_result)

                    if p_value:
                        pvalue = "true"
                    else:
                        pvalue = "false"

                    curr_time = datetime.now()
                    curr_time = str(curr_time)

                    payload = {"Date": curr_time, "IsOccupied": str(pvalue), "ParkingId": str(pid), "Camera": str(key)}
                    payload_json = json.dumps(payload)

                    headers = {
                        'Content-Type': 'application/json', 'charset': 'utf-8'
                    }

                    resp = requests.post("https://api.jnptparking.in/api/Parking/UpdateHourlyParking", data=payload_json, headers=headers, verify=False)
                    # print(key, ": Image POST Status 2 : ", resp.text)
                    # resp = requests.post("http://122.186.213.190:8084/api/Parking/UpdateHourlyParking", data=payload_json, headers = headers, verify=False)

                    # print("Cam : ",str(key), "\tSlot : ",str(pid), "\tResult : ",str(pvalue),"\tPOST Status : ",resp.text)

        time.sleep(5)
        count += 1


def client_main():
    generate_compare_masks()
    main()

# if __name__ == '__main__':
#     generate_compare_masks()
#     main()