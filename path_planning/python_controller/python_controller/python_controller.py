import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class pythonController(Node):

    def __init__(self):
        super().__init__('python_controller')
        self.publisher_ = self.create_publisher(Twist, '/dolly/cmd_vel', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 0.5
        msg.angular.z = 0.3
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: Linear x = %0.2f and Angular z = %0.2f" % (msg.linear.x, msg.angular.z))


def main(args=None):
    rclpy.init(args=args)

    python_controller = pythonController()

    rclpy.spin(python_controller)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    python_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
