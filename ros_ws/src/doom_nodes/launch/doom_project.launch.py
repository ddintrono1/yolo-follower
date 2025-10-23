from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join( 
                    get_package_share_directory('turtlebot3_gazebo'),
                    'launch',
                    'turtlebot3_world.launch.py'
                )
            ),
            launch_arguments={'use_sim_time': 'true'}.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join( 
                    get_package_share_directory('turtlebot3_navigation2'),
                    'launch',
                    'navigation2.launch.py'
                )
            ),
            launch_arguments={
                'use_sim_time': 'true',
                'map': 'saved_maps/hexa_world.yaml'
            }.items()
        ),
        Node(
            package='doom_nodes',
            executable='perceptor',
            name='perceptor',
            output='log',
            parameters=[{'use_sim_time': True}]
        ),
        Node(
            package='doom_nodes',
            executable='localizer',
            name='localizer',
            output='log',
            parameters=[{'use_sim_time': True}]
        ),
        Node(
            package='doom_nodes',
            executable='initial_state_publisher',
            name='initial_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),
        Node(
            package='doom_nodes',
            executable='navigator',
            name='navigator',
            output='screen',
            parameters=[{'use_sim_time': True}]
        )
    ])
