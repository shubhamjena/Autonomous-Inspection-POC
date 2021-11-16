
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

# this is the function launch  system will look for

def generate_launch_description():

    robot_name = 'gazebo'  # robot is the name of the package
    world_file_name = 'empty_area.world'

    # full  path to urdf and world file

    world = os.path.join(get_package_share_directory(robot_name), 'worlds', world_file_name)

    sdf = os.path.join(get_package_share_directory(robot_name), 'models', 'iBot', 'model.sdf')

    # read urdf contents because to spawn an entity in
    # gazebo we need to provide entire sdf as string on  command line

    xml = open(sdf, 'r').read()

    # double quotes need to be with escape sequence
    xml = xml.replace('"', '\\"')

    # this is argument format for spwan_entity service
    spawn_args = {"name": "iBot", "xml": xml}
    #name = "sdf_ball"
    #xml_cmd = "<?xml version=\"1.0\" ?><sdf version=\"1.5\"><model name=\"will_be_ignored\"><static>true</static><link name=\"link\"><visual name=\"visual\"><geometry><sphere><radius>1.0</radius></sphere></geometry></visual></link></model></sdf>"
    #spawn_args = {"name": "sdf_ball", "xml": xml_cmd}
    # wrench_msg = {"link_name": "iBot::robot_footprint", "reference_frame": "", "reference_point": { x: 0, y: 0, z: 0 }, "wrench": { force: { x: 10, y: 0, z: 0 }, torque: { x: 0, y: 0, z: 0 } }, "start_time": {sec: 0, nanosec: 0}, "duration": {sec: -1, nanosec: 0} }
    # create and return launch description object
    return LaunchDescription([

        # start gazebo, notice we are using libgazebo_ros_factory.so instead of libgazebo_ros_init.so
        # That is because only libgazebo_ros_factory.so contains the service call to /spawn_entity
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-u', world, '-s', 'libgazebo_ros_factory.so', '-s', 'libgazebo_ros_force_system.so'],
            output='screen'),

        # tell gazebo to spwan your robot in the world by calling service
        ExecuteProcess(
            cmd=['ros2', 'service', 'call', '/spawn_entity', 'gazebo_msgs/SpawnEntity', str(spawn_args)],
            output='screen'),

# ros2 service call /apply_link_wrench gazebo_msgs/srv/ApplyLinkWrench '{link_name: "iBot::robot_footprint", reference_frame: "", reference_point: { x: 0, y: 0, z: 0 }, wrench: { force: { x: 10, y: 0, z: 0 }, torque: { x: 0, y: 0, z: 0 } }, start_time: {sec: 0, nanosec: 0}, duration: {sec: -1, nanosec: 0} }'

        # tell gazebo to call applying link wrench service
        # ExecuteProcess(
        #     cmd=['ros2', 'service', 'call', '/apply_link_wrench', 'gazebo_msgs/srv/ApplyLinkWrench', '{link_name: "iBot::robot_footprint", reference_frame: "", reference_point: { x: 0, y: 0, z: 0 }, wrench: { force: { x: 0, y: 0, z: 0 }, torque: { x: 0, y: 0, z: 1000 } }, start_time: {sec: 0, nanosec: 0}, duration: {sec: -1, nanosec: 0} }'],
        #     output='screen'),
    ])
