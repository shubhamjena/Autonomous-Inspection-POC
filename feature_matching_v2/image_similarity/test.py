import math
import cv2
import numpy as np
import pandas as pd
from image_similarity_measures.quality_metrics import rmse, ssim, sre
import os

ROUGH_COORDINATES = [
    ['image1', 4.99, -1, 0.2],
    ['image3', 4.99, -1, 0.2],
    ['image6', 4.99, -1, 0.5],
    ['image7', 4.99, -1, 0.1],
    ['image8', 4.99, -0.88, -0.9],
]

INDEX = 1

IMAGE_NAME = ROUGH_COORDINATES[INDEX][0]

ROBOT_COORDINATES = [
    ROUGH_COORDINATES[INDEX][1],
    ROUGH_COORDINATES[INDEX][2],
    ROUGH_COORDINATES[INDEX][3],
]

DISTANCE_WEIGHT = 0.8


DATASET_COORDINATES = "/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/DATABASE_coordinates.csv"
dataset_coordinates = pd.read_csv(DATASET_COORDINATES);

camera_image_path = "/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching_v2/image_similarity/test/" + IMAGE_NAME + ".png"
camera_image = cv2.imread(camera_image_path)

test_img = camera_image


################################################################################################################################################################
#* RMSE, SSIM, SRE METHOD
################################################################################################################################################################

# sre_measures = {}

# scale_percent = 100
# width = int(test_img.shape[1] * scale_percent / 100)
# height = int(test_img.shape[0] * scale_percent / 100)
# dim = (width, height)

# data_dir = 'dataset'
# os.listdir(data_dir)
   
# for file in os.listdir(data_dir):
#     img_path = os.path.join(data_dir, file)
#     data_img = cv2.imread(img_path)
#     resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
#     image_name = file.split('.')[0]
#     dataset_image = dataset_coordinates.loc[dataset_coordinates['Image_Id'] == image_name]
#     image_coordinates = [
#         dataset_image.X.iloc[0],
#         dataset_image.Y.iloc[0],
#         dataset_image.Z.iloc[0],
#     ]
#     distance = math.sqrt(np.sum(np.square(np.array(image_coordinates) - np.array(ROBOT_COORDINATES))))
#     sre_measure = sre(test_img, resized_img)
#     sre_measures[image_name] = sre_measure/pow(distance, DISTANCE_WEIGHT)

# sorted_measures = (dict(sorted(sre_measures.items(), key=lambda item: item[1], reverse = True)))
# closest_image_name = list(sorted_measures.keys())[0]
# print(pd.DataFrame(sorted_measures.items(), columns=['image_id', 'measure'])[:5])

# closest_image = cv2.imread(data_dir + '/' + closest_image_name + '.jpg')
# closest_image = cv2.resize(closest_image, dim, interpolation = cv2.INTER_AREA)


# cv2.imshow('camera image', camera_image)
# cv2.imshow('closest image', closest_image)

################################################################################################################################################################
#* HISTOGRAM METHOD
################################################################################################################################################################

camera_image_hsv = cv2.cvtColor(camera_image, cv2.COLOR_BGR2HSV)

h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]
h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges
channels = [0, 1]

camera_image_hist = cv2.calcHist([camera_image_hsv], channels, None, histSize, ranges, accumulate=False)
cv2.normalize(camera_image_hist, camera_image_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

compare_method = cv2.HISTCMP_CORREL

histogram_measures = {}

scale_percent = 100
width = int(test_img.shape[1] * scale_percent / 100)
height = int(test_img.shape[0] * scale_percent / 100)
dim = (width, height)

data_dir = 'dataset'
os.listdir(data_dir)
   
for file in os.listdir(data_dir):
    img_path = os.path.join(data_dir, file)
    data_img = cv2.imread(img_path)
    resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
    image_name = file.split('.')[0]
    dataset_image = dataset_coordinates.loc[dataset_coordinates['Image_Id'] == image_name]
    image_coordinates = [
        dataset_image.X.iloc[0],
        dataset_image.Y.iloc[0],
        dataset_image.Z.iloc[0],
    ]
    distance = math.sqrt(np.sum(np.square(np.array(image_coordinates) - np.array(ROBOT_COORDINATES))))
    hist_img = cv2.calcHist([hsv_img], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_measure = cv2.compareHist(camera_image_hist, hist_img, compare_method)/pow(distance, DISTANCE_WEIGHT)
    histogram_measures[image_name] = hist_measure

sorted_measures = (dict(sorted(histogram_measures.items(), key=lambda item: item[1], reverse = True)))
closest_image_name = list(sorted_measures.keys())[0]
print(pd.DataFrame(sorted_measures.items(), columns=['image_id', 'measure'])[:5])

closest_image = cv2.imread(data_dir + '/' + closest_image_name + '.jpg')
closest_image = cv2.resize(closest_image, dim, interpolation = cv2.INTER_AREA)


cv2.imshow('camera image', camera_image)
cv2.imshow('closest image', closest_image)

################################################################################################################################################################

cv2.waitKey(0)
cv2.destroyAllWindows()
