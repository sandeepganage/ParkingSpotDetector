import cv2
import json
import requests
import pyodbc
import base64
import time
import os
from PIL import Image

server = 'aaditechdb.database.windows.net'
database = 'JNPT_QA'
username = 'aaditechadmin'
password = 'AadiTech@123'
print('hi')
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = conn.cursor()
# conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=localhost\SQLEXPRESS; Database=ParkingAi; trusted_connection=YES;")


IP = 'http://127.0.0.1'
PORT = '5000'
API = 'get_parking_results'
cameraip = ['rtsp://192.168.1.110:554', 'rtsp://192.168.1.109:554', 'rtsp://192.168.0.102:554',
            'rtsp://192.168.0.103:554', 'rtsp://192.168.0.109:554', 'rtsp://192.168.0.107:554',
            'rtsp://192.168.0.110:554']


def storedb(index):
    if index != "1" and index != "2" and index != "3" and index != "5":
    #if 1 == 1:
        global cameraip
        capture = cv2.VideoCapture(cameraip[int(index)-1] + "/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream")
        ret, image = capture.read()
        print(type(image))

        scale_percent = 20  # percent of original size
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)

        # resize image
        resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
        os.chdir(r'C:\ParkingSpotDetector\Flask\img')
        cv2.imwrite('a.jpg', resized)
        print('/img/a.jpg')
        retval, buffer = cv2.imencode('.jpg', resized)
        with open("a.jpg", "rb") as image:
            image_readed = image.read()
            Byte_image = bytearray(image_readed)
       # newImage = base64.b64encode(resized)


        #capture.release();

        cursor.execute("UPDATE Parking_Image SET UpdateTime = getdate() , LatestImage = ? WHERE Camera = ?",
                       Byte_image, str(index));
        print(index)
        conn.commit();


storedb('1')

def main():
    cam = ""
    pid = ""
    p_value = ""
    pvalue = "0"

    url = IP + ":" + PORT + "/" + API

    count = 0
    while True:
        response = requests.post(url).json()
        print(response)
        if count == 2:
            print(count)
            count = 0
            # logic part
            # For Loop

            for key in response:
                storedb(key)
                result = response.get(key)
                # print(result)
                print(response)
                for spot_result in result:
                    pid = spot_result
                    p_value = result.get(spot_result)

                    if p_value:
                        pvalue = "1"
                    else:
                        pvalue = "0"
                    cam = "C" + key

                    # if key == 1:
                    #     cam = "C1"
                    # if key == 2:
                    #     cam = "C3"
                    # if key == 3:
                    #     cam = "C4"
                    # if key == 4:
                    #     cam = "C5"
                    # if key == 5:
                    #     cam = "C6"
                    # if key == 6:
                    #     cam = "C7"
                    # if key == 7:
                    #     cam = "C8"

                    # print("UPDATE Hourly_Parking_Statistics SET [Date] = getdate(), IsOccupied = " + pvalue + " WHERE ParkingId = '" + str(pid) + "' AND Camera = '" + cam + "'")

                    cursor.execute("UPDATE Hourly_Parking_Statistics SET [Date] = getdate(), IsOccupied = " + pvalue + " WHERE ParkingId = '" + str(pid) + "' AND Camera = '" + cam + "'")
                    conn.commit()

        time.sleep(10)
        count += 1


if __name__ == '__main__':
    main()
