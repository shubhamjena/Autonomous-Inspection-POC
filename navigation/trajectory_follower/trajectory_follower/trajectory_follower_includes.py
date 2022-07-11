import rclpy
import numpy as np
from math import dist, nan
import tf_transformations

from rclpy.node import Node

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu

from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool  # can give string if needed
from sensor_msgs.msg import JointState

reference_position = [5.0, 0.0, 0.0]
n_hat = [1.0, 0.0, 0.0]
yaw_correction = 0.0
ekf_output = Odometry()
estimated_pose = Odometry()
imu = Imu()
orientation = []
orientation_unit = []