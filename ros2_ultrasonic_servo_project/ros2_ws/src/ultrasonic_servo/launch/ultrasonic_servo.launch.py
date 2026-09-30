from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='ultrasonic_servo',
            executable='arduino_bridge',
            name='arduino_bridge',
            output='screen',
            parameters=[
                {
                    'port': '/dev/ttyUSB0',
                    'baud_rate': 115200,
                }
            ],
        ),
        Node(
            package='ultrasonic_servo',
            executable='distance_controller',
            name='distance_controller',
            output='screen',
            parameters=[
                {
                    'threshold_cm': 50.0,
                    'near_angle': 90,
                    'far_angle': 0,
                }
            ],
        ),
    ])
