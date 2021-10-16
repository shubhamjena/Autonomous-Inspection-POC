import os

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_dolly_gazebo = get_package_share_directory('dolly_gazebo')

    # Gazebo Launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument(
        'world',
        default_value = [os.path.join(pkg_dolly_gazebo, 'worlds', 'dolly_empty.world'), ''],
        description = 'SDF world file'),
        gazebo
    ])
