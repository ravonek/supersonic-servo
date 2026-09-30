from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'ultrasonic_servo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name],
        ),
        ('share/' + package_name, ['package.xml']),
        (
            os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py'),
        ),
    ],
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Kaldybekov Adilkhan',
    maintainer_email='aybergen@todo.todo',
    description='ROS 2 ultrasonic sensor and SG90 servo control with Arduino Uno.',
    license='Proprietary',
    entry_points={
        'console_scripts': [
            'arduino_bridge = ultrasonic_servo.arduino_bridge:main',
            'distance_controller = ultrasonic_servo.distance_controller:main',
        ],
    },
)
