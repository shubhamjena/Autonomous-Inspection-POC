from hashlib import new
import rclpy
import cv2
import numpy as np
import pandas as pd
import random as rng

from rclpy.node import Node
from cv_bridge import CvBridge

from cv2 import Mat
from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import Bool  # can give string if needed
from nav_msgs.msg import Odometry

paths = {
    'database': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/DATABASE_test/',
    'camera_images': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/CAMERA_IMAGES/',
    'feature_matches': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/FEATURE_MATCHES/',
    'database_cooredinates': '~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/DATABASE_coordinates_test.csv',
}

match_status = Bool()
ekf_output = Odometry()
controller_output = Odometry()
filtered_img = Image()
matched_pose = Vector3()
