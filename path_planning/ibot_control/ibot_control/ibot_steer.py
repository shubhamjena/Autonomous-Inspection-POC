import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
pos = 0;

class iBotSteer(Node):

    def __init__(self):
        super().__init__('ibot_steer')
        self.publisher_ = self.create_publisher(Twist, '/iBot/cmd_vel', 10)
        self.publisher2_ = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        timer_period = 0.001  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        global pos;
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 1.0
        self.publisher_.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    ibot_steer = iBotSteer()

    rclpy.spin(ibot_steer)
    ibot_steer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
