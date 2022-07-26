from .setpoint_follower_lib import *

class SetpointFollower(Node):
    # Imported Functions
    node_init = node_init
    follow_setpoint_callback = follow_setpoint_callback

    # Subscriber Callbacks
    imu_callback = imu_callback
    odom_callback = odom_callback
    estimated_pose_callback = estimated_pose_callback
    
    # Publisher Callbacks
    velocity_timer_callback = velocity_timer_callback

    # Service Callbacks

    def __init__(self):
        super().__init__('setpoint_follower')
        node_init(self)
        

def main(args=None):
    rclpy.init(args=args)
    setpoint_follower = SetpointFollower()
    rclpy.spin(setpoint_follower)
    rclpy.shutdown()

if __name__ == '__main__':
    main()