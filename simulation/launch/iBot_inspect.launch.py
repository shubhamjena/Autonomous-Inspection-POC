from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    launchDescription = LaunchDescription()

    thrust_provider = Node(
        name='thrust_provider',
        package='thrust_provider',
        executable='thrust_provider',
    )

    trajectory_follower = Node(
        name='trajectory_follower',
        package='trajectory_follower',
        executable='trajectory_follower',
        output='screen'
    )

    feature_matcher = Node(
        name='feature_matcher',
        package='feature_matching',
        executable='feature_matcher',
        output='screen'
    )

    launchDescription.add_action(thrust_provider)
    # launchDescription.add_action(trajectory_follower)
    launchDescription.add_action(feature_matcher)

    return launchDescription
