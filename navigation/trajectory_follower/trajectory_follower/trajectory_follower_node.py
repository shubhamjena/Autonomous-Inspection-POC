from .trajectory_follower_lib import *

class TrajectoryFollower(Node):
    # Imported Functions
    node_init = node_init
    correct_traj_callback = correct_traj_callback

    # Subscriber Callbacks
    imu_callback = imu_callback
    odom_callback = odom_callback
    
    # Publisher Callbacks
    thrust_timer_callback = thrust_timer_callback
    velocity_timer_callback = velocity_timer_callback

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