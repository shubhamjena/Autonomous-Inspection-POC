import rclpy
import numpy as np
from rclpy.node import Node
from nav_msgs.msg import Odometry

ekf_output = Odometry()
noisy_odom = Odometry()
noise = 0.05

class NoiseInjector(Node):
    '''
    Publishes Noisy Odometry Data to "/iBot/noisy_odom" topic
    '''

    def __init__(self):
        super().__init__('noise_injector')
        self.odom_sub = self.create_subscription(Odometry,'/iBot/odometry/filtered',self.odom_callback,1)
        self.noisy_odom_pub = self.create_publisher(Odometry,'/iBot/noisy_odom', 1)
        self.noisy_odom_timer = self.create_timer(1, self.noisy_odom_timer_callback)

    def odom_callback(self, data):
        global ekf_output
        ekf_output = data

    def noisy_odom_timer_callback(self):
        global noisy_odom, noise
        noisy_odom.pose.pose.position.x = ekf_output.pose.pose.position.x + np.random.normal(0, noise)
        noisy_odom.pose.pose.position.y = ekf_output.pose.pose.position.y + np.random.normal(0, noise)
        noisy_odom.pose.pose.position.z = ekf_output.pose.pose.position.z + np.random.normal(0, noise)
        noisy_odom.child_frame_id = 'robot_footprint'
        noisy_odom.header.frame_id = 'odom'
        self.noisy_odom_pub.publish(noisy_odom)

def main(args=None):
    rclpy.init(args=args)
    noise_injector = NoiseInjector()
    rclpy.spin(noise_injector)
    rclpy.shutdown()

if __name__ == '__main__':
    main()