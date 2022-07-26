import rclpy
import numpy as np
from math import dist, nan
import tf_transformations

from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

reference_position = [5.0, 0.0, 0.0]
correction_factor = 5
n_hat = [1.0, 0.0, 0.0]
yaw_correction = 0.0
ekf_output = Odometry()
estimated_pose = Odometry()
imu = Imu()
orientation = []
orientation_unit = []