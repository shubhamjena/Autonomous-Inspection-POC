import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default

from sensor_msgs.msg import LaserScan


class DollyListner(Node):

    def __init__(self):
        super().__init__('dolly_listner')
        self.subscription = self.create_subscription(
            LaserScan,
            'laser_scan',
            self.listener_callback,
            qos_profile=qos_profile_system_default)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%f"' % msg.range_max)


def main(args=None):
    rclpy.init(args=args)

    dolly_listner = DollyListner()

    rclpy.spin(dolly_listner)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    dolly_listner.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
