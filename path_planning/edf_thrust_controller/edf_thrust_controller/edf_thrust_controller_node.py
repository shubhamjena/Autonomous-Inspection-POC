import os
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from gazebo_msgs.srv import ApplyLinkWrench

def main(args=None):
    rclpy.init(args=args)

    print('thrust_controller running.')
    os.system('''ros2 service call /apply_link_wrench gazebo_msgs/srv/ApplyLinkWrench \'{link_name: "iBot::robot_footprint", reference_frame: "iBot::robot_footprint", reference_point: { x: 0.0, y: 0, z: 0 }, wrench: { force: { x: 600, y: 0, z: -600 }, torque: { x: 0, y: 0, z: 0 } }, start_time: {sec: 0, nanosec: 0}, duration: {sec: -1, nanosec: 0} }\'''')
    # os.system('''ros2 service call /apply_link_wrench gazebo_msgs/srv/ApplyLinkWrench \'{link_name: "iBot::robot_footprint", reference_frame: "iBot::robot_footprint", reference_point: { x: 0.1, y: 0, z: 0 }, wrench: { force: { x: 0, y: 1000, z: -300 }, torque: { x: 0, y: 0, z: 0 } }, start_time: {sec: 0, nanosec: 0}, duration: {sec: -1, nanosec: 0} }\'''')


if __name__ == '__main__':
    main()
