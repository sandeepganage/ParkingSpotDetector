
DIR = "C:/ParkingSpotDetector/"
DIR_DATA = "C:/ParkingSpotDetector/data/"
IMG_OUT_SAVE_PATH = DIR_DATA + "camOut/"

userID = 'admin'
password = 'CPPJNPT@123'
available_cams = {1: "rtsp://192.168.1.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 2: "rtsp://192.168.1.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 3: "rtsp://192.168.0.102:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  4: "rtsp://192.168.0.103:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  5: "rtsp://192.168.0.109:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  6: "rtsp://192.168.0.107:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 7: "rtsp://192.168.0.110:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 8: "rtsp://192.168.0.101:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                  # 9: "rtsp://192.168.0.104:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 # 10: "rtsp://192.168.0.105:554/user=admin_password=oyXv12aW_channel=1_stream=0.sdp?real_stream",
                 15: "rtsp://192.168.0.113:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
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
                 # 31: "rtsp://192.168.0.146:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 32: "rtsp://192.168.0.147:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 33: "rtsp://192.168.0.148:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 34: "rtsp://192.168.0.118:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 35: "rtsp://192.168.0.149:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 36: "rtsp://192.168.0.150:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 38: "rtsp://192.168.0.152:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 39: "rtsp://192.168.0.153:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 40: "rtsp://192.168.0.154:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                 41: "rtsp://192.168.0.155:554/user=admin_password=_channel=1_stream=0.sdp?real_stream",
                  }

cam_dimension = (1296, 2304)
available_model = {1: 'PSD_Model_ep0152_loss0.0677.h5'}
decision_threshold = 10