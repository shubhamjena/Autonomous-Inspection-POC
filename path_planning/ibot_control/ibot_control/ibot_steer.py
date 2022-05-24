import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class iBotSteer(Node):

    def __init__(self):
        super().__init__('ibot_steer')
        self.publisher_ = self.create_publisher(Twist, '/iBot/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        twist = Twist()
        twist.linear.x = 0.0
        self.publisher_.publish(twist)
        self.get_logger().info("Publishing: Vx of %0.2f m/s" % (twist.linear.x))


def main(args=None):
    rclpy.init(args=args)

    ibot_steer = iBotSteer()

    rclpy.spin(ibot_steer)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ibot_steer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
