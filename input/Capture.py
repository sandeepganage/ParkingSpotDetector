import cv2
import time
from datetime import datetime
from datetime import date
import os


available_cams = {1: "rtsp://192.168.1.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 2: "rtsp://192.168.1.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 3: "rtsp://192.168.0.102:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  4: "rtsp://192.168.0.103:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 5: "rtsp://192.168.0.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  6: "rtsp://192.168.0.107:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 7: "rtsp://192.168.0.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 8: "rtsp://192.168.0.101:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 9: "rtsp://192.168.0.104:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 # 10: "rtsp://192.168.0.105:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 # 15: "rtsp://192.168.0.113:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 16: "rtsp://192.168.0.119:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 17: "rtsp://192.168.0.120:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 18: "rtsp://192.168.0.123:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 19: "rtsp://192.168.0.124:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 20: "rtsp://192.168.0.125:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 21: "rtsp://192.168.0.126:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 22: "rtsp://192.168.0.127:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 23: "rtsp://192.168.0.128:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 # 24: "rtsp://192.168.0.202:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 # 25: "rtsp://192.168.0.140:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 # 26: "rtsp://192.168.0.141:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 27: "rtsp://192.168.0.142:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 # 28: "rtsp://192.168.0.143:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 # 29: "rtsp://192.168.0.144:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 30: "rtsp://192.168.0.145:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 31: "rtsp://192.168.0.146:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 32: "rtsp://192.168.0.147:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 33: "rtsp://192.168.0.148:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 34: "rtsp://192.168.0.118:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 35: "rtsp://192.168.0.149:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 36: "rtsp://192.168.0.150:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 # 37: "rtsp://192.168.0.151:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 38: "rtsp://192.168.0.152:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 39: "rtsp://192.168.0.153:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 40: "rtsp://192.168.0.154:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 41: "rtsp://192.168.0.155:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                }


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

