import rclpy
import pandas as pd
from math import dist

from rclpy.node import Node

from geometry_msgs.msg import Vector3
from geometry_msgs.msg import PoseArray
from geometry_msgs.msg import Pose
from std_msgs.msg import Bool  # can give string if needed
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState

from std_srvs.srv import Trigger

X = 0.5

matched_status = Bool()
ekf_pose = Odometry()
matched_pose = Odometry()
truth_pose = Odometry()
merged_pose = Vector3()

benchmarks_path = '/home/atharva/ros2/airbus_ws/src/Autonomous-Inspection-POC/pose_merger/data/benchmark/poses.csv'

truth_array = []
truth_array.append([])
truth_array.append([])

merged_array = []
merged_array.append([])
merged_array.append([])

ekf_array = []
ekf_array.append([])
ekf_array.append([])

a = JointState()
a.velocity.append(1)
print(a)