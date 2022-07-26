from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    launchDescription = LaunchDescription()

    ibot_steer = Node(
        package="ibot_control",
        executable="ibot_steer",
    )

    ibot_edf_thrust_control = Node(
        package="ibot_control",
        executable="ibot_edf_thrust_control"
    )

    launchDescription.add_action(ibot_edf_thrust_control)
    launchDescription.add_action(ibot_steer)

    return launchDescription
