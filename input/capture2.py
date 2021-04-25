import cv2
import time
from datetime import datetime
import os
from matplotlib import pyplot
#os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"

# capture = cv2.VideoCapture('rtsp://admin:p@$$w0rd123@122.200.22.250:8001')
# # capture = cv2.VideoCapture('rtsp://admin: @192.168.1.108:8001')
# video = cv2.VideoCapture('rtsp://service:Jnpt_123@192.168.0.58')
IsImages = 1
count = 0
counter = 0
while True:
    counter = 2000
    if counter == 2000:
        counter = 0
        # capture = cv2.VideoCapture('rtsp://admin:p@$$w0rd123@122.200.22.250:8003')
        # capture = cv2.VideoCapture('rtsp://admin:CPPJNPT@123@192.168.1.110:8003/video')
        # capture = cv2.VideoCapture('rtsp://192.168.1.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream')
        capture = cv2.VideoCapture('rtsp://192.168.0.127:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream')
        if not capture.isOpened():
            print("Can't open stream/file")
        else:
            ret, frame = capture.read()

            tile = cv2.cvtColor(frame, 0)
            # pyplot.imshow(tile)
            # pyplot.show()
            tile_number = (str(datetime.now())).split(" ")
            tile_number = tile_number[0] + "_" + tile_number[1]
            tile_number = tile_number.split(".")[0]
            tile_number = tile_number.replace(":", "_")
            cv2.imwrite("D:/Trial/" + tile_number + ".png", tile)
            print(tile_number)
            time.sleep(120)
            cv2.destroyAllWindows()

