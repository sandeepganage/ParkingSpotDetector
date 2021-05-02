
DIR = "C:/ParkingSpotDetector/"
DIR_DATA = "C:/ParkingSpotDetector/data/"
IMG_OUT_SAVE_PATH = DIR_DATA + "camOut/"

userID = 'admin'
password = 'CPPJNPT@123'
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
                 22: "rtsp://192.168.0.127:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 23: "rtsp://192.168.0.202:554/user=admin_password=_channel=1_stream=0.sdp?real_stream"}

cam_dimension = (1296, 2304)
available_model = {1: 'PSD_Model_ep0152_loss0.0677.h5'}
decision_threshold = 10