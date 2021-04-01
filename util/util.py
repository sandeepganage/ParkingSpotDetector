
DIR = "C:/ParkingSpotDetector/"
DIR_DATA = "C:/ParkingSpotDetector/data/"
userID = 'admin'
password = 'CPPJNPT@123'
available_cams = {1: "rtsp://192.168.1.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  2: "rtsp://192.168.1.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream"}
cam_dimension = {1: (1296, 2304), 2: (1296, 2304)}
available_model = {1: 'mask_rcnn_containers_0076.h5'}
decision_threshold = 10