import time
import serial

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_msgs.msg import Int16


class ArduinoBridge(Node):
    """Bridge between Arduino serial messages and ROS 2 topics."""

    def __init__(self):
        super().__init__('arduino_bridge')

        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baud_rate', 115200)

        port = self.get_parameter('port').value
        baud_rate = self.get_parameter('baud_rate').value

        self.serial_port = serial.Serial(
            port,
            baud_rate,
            timeout=0.01
        )

        # Arduino Uno normally resets when the serial port is opened.
        time.sleep(2)

        self.distance_pub = self.create_publisher(
            Float32,
            '/distance_cm',
            10
        )

        self.servo_sub = self.create_subscription(
            Int16,
            '/servo_angle',
            self.servo_callback,
            10
        )

        self.timer = self.create_timer(
            0.02,
            self.read_arduino
        )

        self.get_logger().info(
            f'Arduino bridge started on {port} at {baud_rate} baud'
        )

    def read_arduino(self):
        if self.serial_port.in_waiting <= 0:
            return

        line = self.serial_port.readline()

        try:
            line = line.decode().strip()
        except UnicodeDecodeError:
            return

        # Arduino sends: D:34.5
        if line.startswith('D:'):
            try:
                distance = float(line[2:])
            except ValueError:
                return

            msg = Float32()
            msg.data = distance
            self.distance_pub.publish(msg)

            self.get_logger().info(
                f'Distance: {distance:.1f} cm'
            )

    def servo_callback(self, msg):
        angle = max(0, min(180, int(msg.data)))
        command = f'S:{angle}\n'
        self.serial_port.write(command.encode())
        self.serial_port.flush()

        self.get_logger().info(
            f'Servo command: {angle} degrees'
        )

    def close_serial(self):
        if self.serial_port.is_open:
            self.serial_port.close()


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.close_serial()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
