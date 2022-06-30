from .trajectory_follower_lib import *

class TrajectoryFollower(Node):
    # Imported Functions
    node_init = node_init
    thrust_timer_callback = thrust_timer_callback
    velocity_timer_callback = velocity_timer_callback

    # Subscriber Callbacks
    
    # Publisher Callbacks

    # Service Callbacks

    def __init__(self):
        super().__init__('trajectory_follower')
        node_init(self)
        

def main(args=None):
    rclpy.init(args=args)
    trajectory_follower = TrajectoryFollower()
    rclpy.spin(trajectory_follower)
    rclpy.shutdown()

if __name__ == '__main__':
    main()