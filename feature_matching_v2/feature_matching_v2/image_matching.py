import math
import cv2
import numpy as np
import pandas as pd
from image_similarity_measures.quality_metrics import rmse, ssim, sre
import os

def MatchImageHistogram(image, data_dir, robot_coordinates):
    #* PARAMETERS

    DISTANCE_WEIGHT = 1
    FIRST_N_IMAGES = 3
    DISTANCE_THRESHOLD = 0.4
    DISTANCE_SCALE = 1
    CESSNA_HEIGHT = 5
    K_x = 1 
    K_y = 1
    K_z = 1

    DATASET_COORDINATES = "/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching_v2/image_similarity/csv/dataset_coordinates.csv"
    dataset_coordinates = pd.read_csv(DATASET_COORDINATES);

    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges
    channels = [0, 1]
    compare_method = cv2.HISTCMP_CORREL

    histogram_measures = {}
    estimated_z = -1000000000

    camera_img = image
    camera_img_hsv = cv2.cvtColor(camera_img, cv2.COLOR_RGB2HSV)
    camera_img_hist = cv2.calcHist([camera_img_hsv], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(camera_img_hist, camera_img_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    #* PREPARE SCALE DIMENSIONS

    scale_percent = 100
    width = int(camera_img.shape[1] * scale_percent / 100)
    height = int(camera_img.shape[0] * scale_percent / 100)
    dim = (width, height)

    #* IMAGE MATCHING USING HISTOGRAM AND DISTANCE THRESHOLDING

    data_dir = '/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching_v2/image_similarity/processed_dataset'
    
    if robot_coordinates[0] == 0 and robot_coordinates[1] == 0 and robot_coordinates[2] == 6.9:
        return [], [], estimated_z

    def calc_dist(p, q):
        x_c = K_x*(pow(p[0] - q[0], 2))
        y_c = K_y*(pow(p[1] - q[1], 2))
        z_c = K_z*(pow(p[2] - q[2], 2))
        return math.sqrt(x_c + y_c + z_c)

    for file in os.listdir(data_dir):
        img_path = os.path.join(data_dir, file)
        hsv_img = cv2.imread(img_path)
        image_name = file.split('.')[0]
        dataset_image = dataset_coordinates.loc[dataset_coordinates['Image_Id'] == image_name]
        image_coordinates = [
            dataset_image.X.iloc[0],
            dataset_image.Y.iloc[0],
            dataset_image.Z.iloc[0] + CESSNA_HEIGHT,
        ]
        distance = calc_dist(image_coordinates, robot_coordinates)
        if distance > DISTANCE_THRESHOLD:
            continue
        distance_scaled = distance + DISTANCE_SCALE
        hist_img = cv2.calcHist([hsv_img], channels, None, histSize, ranges, accumulate=False)
        cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        hist_measure = cv2.compareHist(camera_img_hist, hist_img, compare_method)/pow(distance_scaled, DISTANCE_WEIGHT)
        histogram_measures[image_name] = hist_measure

    #* ADDITIONAL CHECKS TO IMPROVE ACCURACY

    closest_img_names = []
    closest_imgs = []
    closest_img_coordinates = []
    closest_distances = []

    closest_img_coordinate = []
    closest_img_name = []

    distance = 100000000

    sorted_measures = (dict(sorted(histogram_measures.items(), key=lambda item: item[1], reverse = True)))
    closest_img_names = list(sorted_measures.keys())[0 : FIRST_N_IMAGES]

    for index, value in enumerate(closest_img_names):
        closest_imgs.append(dataset_coordinates.loc[dataset_coordinates['Image_Id'] == closest_img_names[index]])
        closest_img_coordinates.append([
            closest_imgs[index].X.iloc[0],
            closest_imgs[index].Y.iloc[0],
            closest_imgs[index].Z.iloc[0] + CESSNA_HEIGHT,
        ])
        closest_distances.append(calc_dist(closest_img_coordinates[index], robot_coordinates))
        if closest_distances[index] < distance:
            distance = closest_distances[index]
            closest_img_name = closest_img_names[index]
            closest_img_coordinate = closest_img_coordinates[index]

    if len(closest_img_coordinates) < 1:
        return [], [], estimated_z
    estimated_z = (np.sum(closest_img_coordinates[0:2], axis=0)[2]/len(closest_img_coordinates))
    # print(closest_img_names)

    #* FINAL DISTANCE CHECK BEFORE PUBLISHING

    distance = math.sqrt(np.sum(np.square(np.array(closest_img_coordinate) - np.array(robot_coordinates))))
    if distance > DISTANCE_THRESHOLD:
        return [], [], estimated_z
    else:
        return closest_img_coordinate, closest_img_name, estimated_z

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

# camera_image_hsv = cv2.cvtColor(camera_image, cv2.COLOR_BGR2HSV)

# h_bins = 50
# s_bins = 60
# histSize = [h_bins, s_bins]
# h_ranges = [0, 180]
# s_ranges = [0, 256]
# ranges = h_ranges + s_ranges
# channels = [0, 1]

# camera_image_hist = cv2.calcHist([camera_image_hsv], channels, None, histSize, ranges, accumulate=False)
# cv2.normalize(camera_image_hist, camera_image_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

# compare_method = cv2.HISTCMP_CORREL

# histogram_measures = {}

# scale_percent = 100
# width = int(test_img.shape[1] * scale_percent / 100)
# height = int(test_img.shape[0] * scale_percent / 100)
# dim = (width, height)

# data_dir = '../image_similarity/dataset'
# os.listdir(data_dir)
   
# for file in os.listdir(data_dir):
#     img_path = os.path.join(data_dir, file)
#     data_img = cv2.imread(img_path)
#     resized_img = cv2.resize(data_img, dim, interpolation = cv2.INTER_AREA)
#     hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)
#     image_name = file.split('.')[0]
#     dataset_image = dataset_coordinates.loc[dataset_coordinates['Image_Id'] == image_name]
#     image_coordinates = [
#         dataset_image.X.iloc[0],
#         dataset_image.Y.iloc[0],
#         dataset_image.Z.iloc[0],
#     ]
#     distance = math.sqrt(np.sum(np.square(np.array(image_coordinates) - np.array(ROBOT_COORDINATES))))
#     hist_img = cv2.calcHist([hsv_img], channels, None, histSize, ranges, accumulate=False)
#     cv2.normalize(hist_img, hist_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
#     hist_measure = cv2.compareHist(camera_image_hist, hist_img, compare_method)/pow(distance, DISTANCE_WEIGHT)
#     histogram_measures[image_name] = hist_measure

# sorted_measures = (dict(sorted(histogram_measures.items(), key=lambda item: item[1], reverse = True)))
# closest_image_name = list(sorted_measures.keys())[0]
# print(pd.DataFrame(sorted_measures.items(), columns=['image_id', 'measure'])[:5])

# closest_image = cv2.imread(data_dir + '/' + closest_image_name + '.jpg')
# closest_image = cv2.resize(closest_image, dim, interpolation = cv2.INTER_AREA)

################################################################################################################################################################

# cv2.waitKey(0)
# cv2.destroyAllWindows()
