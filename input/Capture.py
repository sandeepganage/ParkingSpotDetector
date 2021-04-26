import cv2
import time
from datetime import datetime
from datetime import date
import os


available_cams = {1: "rtsp://192.168.1.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  2: "rtsp://192.168.1.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  3: "rtsp://192.168.0.102:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  4: "rtsp://192.168.0.103:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  5: "rtsp://192.168.0.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  6: "rtsp://192.168.0.107:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  7: "rtsp://192.168.0.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 16: "rtsp://192.168.0.119:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 17: "rtsp://192.168.0.120:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 18: "rtsp://192.168.0.123:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 19: "rtsp://192.168.0.124:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 20: "rtsp://192.168.0.125:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 21: "rtsp://192.168.0.126:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 22: "rtsp://192.168.0.127:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream"}


# 13: "rtsp://192.168.0.111:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
# 14: "rtsp://192.168.0.112:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
# 15: "rtsp://192.168.0.113:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",


out_dir = "D:/capture/"

IsImages = 1
count = 0
counter = 0
while True:
    counter = 2000
    for cam_id in available_cams:
        ip = available_cams.get(cam_id)
        capture = cv2.VideoCapture(ip)
        if not capture.isOpened():
            print("********** Streaming not working : Cam ID : ", str(cam_id))
        else:
            ret, frame = capture.read()

            today = date.today()
            d = today.strftime("%d_%m_%Y")

            date_dir = out_dir + str(d)
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)

            cam_dir = date_dir + "/" + "cam" + str(cam_id)
            if not os.path.exists(cam_dir):
                os.makedirs(cam_dir)

            tile = cv2.cvtColor(frame, 0)
            tile_number = (str(datetime.now())).split(" ")
            tile_number = tile_number[0] + "_" + tile_number[1]
            tile_number = tile_number.split(".")[0]
            tile_number = tile_number.replace(":", "_")
            cv2.imwrite(cam_dir + "/" + tile_number + ".png", tile)
            print("Stream captured saved for cam : ", str(cam_id))
            cv2.destroyAllWindows()

    time.sleep(120)

