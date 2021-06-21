import cv2
from datetime import datetime
from datetime import date
import multiprocessing
import os
import time

# available_cams = {68: "rtsp://192.168.0.168:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",}
available_cams = {
                     1: "rtsp://192.168.0.101:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     2: "rtsp://192.168.0.102:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     3: "rtsp://192.168.0.103:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     4: "rtsp://192.168.0.104:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     5: "rtsp://192.168.0.105:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     6: "rtsp://192.168.0.106:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     7: "rtsp://192.168.0.107:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     8: "rtsp://192.168.0.108:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                     9: "rtsp://192.168.0.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    10: "rtsp://192.168.0.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    11: "rtsp://192.168.0.111:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    12: "rtsp://192.168.0.112:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    13: "rtsp://192.168.0.113:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    14: "rtsp://192.168.0.114:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    15: "rtsp://192.168.0.115:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    16: "rtsp://192.168.0.116:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    17: "rtsp://192.168.0.117:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    18: "rtsp://192.168.0.118:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    19: "rtsp://192.168.0.119:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    20: "rtsp://192.168.0.120:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    21: "rtsp://192.168.0.121:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    22: "rtsp://192.168.0.122:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    23: "rtsp://192.168.0.123:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    24: "rtsp://192.168.0.124:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    25: "rtsp://192.168.0.125:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    26: "rtsp://192.168.0.126:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    27: "rtsp://192.168.0.127:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    28: "rtsp://192.168.0.128:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    29: "rtsp://192.168.0.129:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    30: "rtsp://192.168.0.130:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    31: "rtsp://192.168.0.131:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    32: "rtsp://192.168.0.132:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    33: "rtsp://192.168.0.133:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    34: "rtsp://192.168.0.134:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    35: "rtsp://192.168.0.135:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    36: "rtsp://192.168.0.136:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    37: "rtsp://192.168.0.137:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    38: "rtsp://192.168.0.138:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    39: "rtsp://192.168.0.139:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    40: "rtsp://192.168.0.140:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    41: "rtsp://192.168.0.141:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    42: "rtsp://192.168.0.142:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    43: "rtsp://192.168.0.143:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    44: "rtsp://192.168.0.144:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    45: "rtsp://192.168.0.145:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    46: "rtsp://192.168.0.146:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    47: "rtsp://192.168.0.147:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    48: "rtsp://192.168.0.148:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    49: "rtsp://192.168.0.149:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    50: "rtsp://192.168.0.150:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    51: "rtsp://192.168.0.151:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    52: "rtsp://192.168.0.152:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    53: "rtsp://192.168.0.153:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    54: "rtsp://192.168.0.154:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    55: "rtsp://192.168.0.155:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    56: "rtsp://192.168.0.156:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    57: "rtsp://192.168.0.157:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    58: "rtsp://192.168.0.158:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    59: "rtsp://192.168.0.159:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    60: "rtsp://192.168.0.160:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    61: "rtsp://192.168.0.161:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    62: "rtsp://192.168.0.162:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    63: "rtsp://192.168.0.163:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    64: "rtsp://192.168.0.164:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    65: "rtsp://192.168.0.165:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    66: "rtsp://192.168.0.166:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    67: "rtsp://192.168.0.167:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    68: "rtsp://192.168.0.168:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    69: "rtsp://192.168.0.169:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    70: "rtsp://192.168.0.170:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    71: "rtsp://192.168.0.171:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                    72: "rtsp://192.168.0.172:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream"
                }


def func(ip, cam_status, mutex):
    capture = cv2.VideoCapture(ip)
    ret, frame = capture.read()
    if ret:
        mutex.acquire()
        cam_status[0] = True
        mutex.release()


def main():
    out_dir = "C:/capture/"
    while True:
        for cam_id in available_cams:
            manager = multiprocessing.Manager()
            mutex = manager.Lock()
            cam_status = manager.dict()
            cam_status[0] = False

            url = available_cams.get(cam_id)
            process = multiprocessing.Process(target=func, args=(url, cam_status, mutex, ))
            process.start()
            time.sleep(5)
            process.terminate()

            IP = (url.split(":554")[0]).split("rtsp://")[1]

            if not cam_status.get(0):
                print("Not working IP: ", str(IP))
            else:
                capture = cv2.VideoCapture(url)
                ret, frame = capture.read()

                if ret:
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
                    print("Working IP : ", str(IP))
                    cv2.destroyAllWindows()

        time.sleep(60)


if __name__ == '__main__':
    main()