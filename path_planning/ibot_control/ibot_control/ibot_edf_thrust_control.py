import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Wrench


class iBotEdfThrustControl(Node):

    def __init__(self):
        super().__init__('ibot_edf_thrust_control')
        self.publisher_ = self.create_publisher(Wrench, '/iBot/gazebo_ros_force', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        wrench = Wrench()
        wrench.force.z = -1000.0
        self.publisher_.publish(wrench)
        self.get_logger().info("Publishing: Thrust force of %0.2f N" % (wrench.force.z))


def main(args=None):
    rclpy.init(args=args)

    ibot_edf_thrust_control = iBotEdfThrustControl()

    rclpy.spin(ibot_edf_thrust_control)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    ibot_edf_thrust_control.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
