from .pose_merger_lib import *

class PoseMerger(Node):
    # Imported Functions
    node_init = node_init

    # Subscriber Callbacks
    truth_callback = truth_callback
    odom_callback = odom_callback
    matched_pose_callback = matched_pose_callback
    matched_status_callback = matched_status_callback
    
    # Publisher Callbacks
    merged_pose_timer_callback = merged_pose_timer_callback
    plot_timer_callback = plot_timer_callback

    # Service Callbacks
    save_pose_data_callback = save_pose_data_callback

    def __init__(self):
        super().__init__('pose_merger')
        node_init(self)
        

def main(args=None):
    rclpy.init(args=args)
    pose_merger = PoseMerger()
    rclpy.spin(pose_merger)
    rclpy.shutdown()

if __name__ == '__main__':
    main()