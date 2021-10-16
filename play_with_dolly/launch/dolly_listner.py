from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    dolly_listner = Node(
        package='play_with_dolly',
        namespace='dolly_listner',
        executable='dolly_listner',
        output='screen',
        remappings=[
            ('laser_scan', '/dolly/laser_scan'),
        ]
    )

    return LaunchDescription([
        dolly_listner
    ])
