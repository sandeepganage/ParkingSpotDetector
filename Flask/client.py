import cv2
import requests
import pyodbc
import time
import os
from util.util import IMG_OUT_SAVE_PATH, DIR_DATA

# "MyProjectConnection": "server=tcp:rit-dbsvr-01.database.windows.net;database=JNPT;User id=ritdbadmin@rit-dbsvr-01;password=Aez@3105.db"


server = 'tcp:rit-dbsvr-01.database.windows.net'
database = 'JNPT'
username = 'ritdbadmin@rit-dbsvr-01'
password = 'Aez@3105.db'

#server = 'aaditechdb.database.windows.net'
#database = 'JNPT_QA'
#username = 'aaditechadmin'
#password = 'AadiTech@123'

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor = conn.cursor()
# conn = pyodbc.connect("DRIVER={SQL Server}; SERVER=localhost\SQLEXPRESS; Database=ParkingAi; trusted_connection=YES;")


IP = 'http://127.0.0.1'
PORT = '5000'
API = 'get_parking_results'
API_CamStatus = 'get_active_cams'

# dict = {'1':'1', '13':'2', '21':'3', '23':'4', '24':'5', '34':'6', '42':'7', '43':'8', '56':'9', '57':'10',
#         '58':'11', '59':'12', '62':'13', '63':'14', '64':'15', '65':'16', '67':'17'}


def storedb(key, camIP,isCamUP):
    CAM_IMG_PATH = str(IMG_OUT_SAVE_PATH) + str(key) + "/0_rgb.jpg"
    image = cv2.imread(CAM_IMG_PATH)
    print(CAM_IMG_PATH)
    scale_percent = 20  # percent of original size
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    image_bytes = cv2.imencode('.jpg', resized)[1].tobytes()
    #print("UPDATE Parking_Image SET UpdateTime = getdate()  WHERE  image_bytes, str(key)" + str(key) + str(camIP) + isCamUP)
    #cursor.execute("UPDATE Parking_Image SET UpdateTime = getdate() , LatestImage = ?, IPAddress = ?, IsLive = ? WHERE Camera = ?", image_bytes, str(camIP), isCamUP, str(key));

    retry_flag = True
    retry_count = 0
    while retry_flag and retry_count < 5:
        try:
            cursor.execute(
                "UPDATE Parking_Image SET UpdateTime = getdate() , LatestImage = ?, IsLive = ? WHERE Camera = ?",
                image_bytes, isCamUP, str(key));
            retry_flag = False
        except:
            print("Retry after 1 sec")
            retry_count = retry_count + 1
            time.sleep(1)

    conn.commit();


def main():
    url = IP + ":" + PORT + "/" + API
    url_camStatus = IP + ":" + PORT + "/" + API_CamStatus

    count = 0
    while True:
        response = requests.post(url).json()
        response_camStatus = requests.post(url_camStatus).json()
        response_camStatus = requests.post(url_camStatus).json()
        print(response)
        if count == 2:
            print(count)
            count = 0
            # logic part
            # For Loop

            strQuery = ""
            for key in response:
                tuple = response_camStatus.get(key)
                isCamUP = tuple[0]
                camIP = str(tuple[1])

                if isCamUP:
                    isCamUP = "1"
                else:
                    isCamUP = "0"
                storedb(key, camIP,isCamUP)
                result = response.get(key)
                # print(result)
                print(response)

                cam_status = 0
                if response_camStatus.get(key):
                    cam_status = 1
                for spot_result in result:
                    pid = spot_result
                    p_value = result.get(spot_result)

                    if p_value:
                        pvalue = "1"
                    else:
                        pvalue = "0"

                    # print("UPDATE Hourly_Parking_Statistics SET [Date] = getdate(), IsOccupied = " + pvalue + " WHERE ParkingId = '" + str(pid) + "' AND Camera = '" + cam + "'")

                    # isCamUP =  : Camera down / up
                    # camIP = Camera IP
                    strQuery = strQuery + "UPDATE Hourly_Parking_Statistics SET [Date] = getdate(), IsOccupied = " + pvalue + " WHERE ParkingId = '" + str(pid) + "' AND Camera = '" + key + "';"

                print(strQuery)
                retry_flag = True
                retry_count = 0
                while retry_flag and retry_count < 5:
                    try:
                        cursor.execute(strQuery)
                        retry_flag = False
                    except:
                        print("Retry after 1 sec")
                        retry_count = retry_count + 1
                        time.sleep(1)

                conn.commit()

        time.sleep(10)
        count += 1


if __name__ == '__main__':
    main()
