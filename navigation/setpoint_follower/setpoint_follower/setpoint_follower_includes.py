import rclpy
import numpy as np
from math import dist, nan
import tf_transformations

from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

reference_position = [5.0, 0.0, 0.0]
correction_factor = 2.0
X = [1.0, 0.0, 0.0]
n_hat = [0.0, 0.0, 1.0]
# setpoints = [
#     [5, 0.3, 6.865],
#     [5, 0.5, 6.78],
#     [5, 0.8, 6.6],
#     [5, 1.0, 6.39],
# ]
setpoints = [
    [5.0, 0.5, 6.78],
    [6.0, 0.5, 6.78],
    [6.0, 0.0, 6.9],
    [5.0, 0.0, 6.9],
]
setpoints_length = len(setpoints)
current_setpoint_number = 0
correction_vector_bot_frame = [0.0, 0.0, 0.0]
current_setpoint = setpoints[0]
yaw_correction = 0.0
ekf_output = Odometry()
estimated_pose = Odometry()
imu = Imu()
twist = Twist()
orientation = []
orientation_unit = []