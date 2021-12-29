import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    pkg_share = FindPackageShare(package='gazebo').find('gazebo')
    default_model_path = os.path.join(pkg_share, 'models/urdf/iBot.urdf')
    world_file_name = 'empty_area.world'
    world_path = os.path.join(pkg_share, 'worlds', world_file_name)

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time'), 'robot_description': Command(['xacro ', LaunchConfiguration('model')])}],
        arguments=[default_model_path],
        remappings=[('/joint_states', '/iBot/joint_states')]
    )

    # joint state publisher already included as a plugin in iBot.gazebo file

    # joint_state_publisher_node = launch_ros.actions.Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    #     #condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui'))
    #)

    spawn_entity = launch_ros.actions.Node(
    	package='gazebo_ros',
    	executable='spawn_entity.py',
        arguments=['-entity', 'iBot' , '-topic', 'robot_description', '-x', '5', '-y', '0', '-z', '0.3', '-R', '0', '-P', '0', '-Y', '1.57' ],
        output='screen'
    )

    robot_localization_node = launch_ros.actions.Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    return launch.LaunchDescription([
        #launch.actions.DeclareLaunchArgument(name='gui', default_value='True',
        #                                    description='Flag to enable joint_state_publisher_gui'),
        launch.actions.DeclareLaunchArgument(name='model', default_value=default_model_path,
                                            description='Absolute path to robot urdf file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so', world_path], output='screen'),

        #joint_state_publisher_node,
        spawn_entity,
        robot_state_publisher_node,
        robot_localization_node

    ])
