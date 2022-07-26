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

    state_estimator = Node(
        name='state_estimator',
        package='state_estimation',
        executable='state_estimator',
        output='screen'
    )

    launchDescription.add_action(thrust_provider)
    # launchDescription.add_action(trajectory_follower)
    launchDescription.add_action(state_estimator)

    return launchDescription
