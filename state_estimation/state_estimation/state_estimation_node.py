from .state_estimation_lib import *

class StateEstimator(Node):
    # Imported Functions
    node_init = node_init

    # Subscriber Callbacks
    camera_image_callback = camera_image_callback
    odom_callback = odom_callback
    ibot_odom_callback = ibot_odom_callback
    velocity_callback = velocity_callback
    imu_callback = imu_callback

    # Publisher Callbacks
    match_status_timer_callback = match_status_timer_callback
    match_position_timer_callback = match_position_timer_callback
    filtered_image_timer_callback = filtered_image_timer_callback
    pose_fusion_timer_callback = pose_fusion_timer_callback

    def __init__(self):
        super().__init__('state_estimator')
        node_init(self)
        

def main(args=None):
    rclpy.init(args=args)
    state_estimator = StateEstimator()
    rclpy.spin(state_estimator)
    rclpy.shutdown()

if __name__ == '__main__':
    main()