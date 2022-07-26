import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Wrench


class ThrustProvider(Node):

    def __init__(self):
        super().__init__('thrust_provider')
        self.publisher_ = self.create_publisher(Wrench, '/iBot/gazebo_ros_force', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        wrench = Wrench()
        wrench.force.z = -1000.0
        self.publisher_.publish(wrench)


def main(args=None):
    rclpy.init(args=args)

    thrust_provider = ThrustProvider()

    rclpy.spin(thrust_provider)
    
    thrust_provider.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
