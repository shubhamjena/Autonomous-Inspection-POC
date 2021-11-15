import os
import sys
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Wrench
from gazebo_msgs.srv import ApplyLinkWrench

def main(args=None):
    rclpy.init(args=args)
    print('thrust_controller running.')
    os.system('''ros2 topic pub /iBot/gazebo_ros_force geometry_msgs/Wrench  \'{force:  {x: 0 , y: 0.0, z: -1000}, torque: {x: 0.0,y: 0.0,z: 0}}\' ''')

if __name__ == '__main__':
    main()
