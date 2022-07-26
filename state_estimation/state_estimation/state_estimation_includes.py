import rclpy
import cv2
import math
import tf_transformations
import pandas as pd
import numpy as np
from datetime import datetime

from rclpy.node import Node
from cv_bridge import CvBridge
from .image_matching import MatchImageHistogram

from sensor_msgs.msg import Image
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from std_msgs.msg import Float64
from nav_msgs.msg import Odometry

paths = {
    'database': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/state_estimation/DATABASE_test/',
    'camera_images': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/state_estimation/CAMERA_IMAGES/',
    'feature_matches': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/state_estimation/FEATURE_MATCHES/',
    'database_coordinates': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/state_estimation/DATABASE_coordinates_test.csv',
}

DATASET_COORDINATES = "/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/state_estimation/image_similarity/csv/dataset_coordinates.csv"
dataset_coordinates = pd.read_csv(DATASET_COORDINATES);

timer_period = 0.1
CESSNA_HEIGHT = 5

match_status = Bool()
ekf_output = Odometry()
controller_output = Odometry()
estimated_pose = Odometry()
filtered_img = Image()
matched_pose = Vector3()
estimated_z = Float64()
velocity = Twist()
imu = Imu()
rotated_vector_in_bot_frame = []
orientation = []
orientation_unit = []
R = []
fallback = False

matched_pose.x = float(-1000)
matched_pose.y = float(-1000)
matched_pose.z = float(-1000)

estimated_z.data = float(6.9)
temp_z = float(6.9)

robot_coordinates = [
    ekf_output.pose.pose.position.x,
    ekf_output.pose.pose.position.y,
    estimated_z.data,
]

''' Pose Fuser Variables '''
fused_pose = Odometry()
initial_time = datetime.now()
current_time = datetime.now()
delta_t = 0.0
v = 0.0
rotated_vector_in_global_frame = [5, 0, 0]