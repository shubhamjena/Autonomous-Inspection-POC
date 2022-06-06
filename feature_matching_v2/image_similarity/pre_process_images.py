import cv2
import os

dim = (800, 800)

data_dir = '/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching_v2/image_similarity/better_dataset'
os.chdir('/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching_v2/image_similarity/hsv_better_dataset')

for file in os.listdir(data_dir):
    img_path = os.path.join(data_dir, file)
    data_img = cv2.imread(img_path)
    resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
    cv2.imwrite(file, hsv_img)