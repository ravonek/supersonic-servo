import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from std_msgs.msg import Int16


class DistanceController(Node):
    """Convert ultrasonic distance into a servo angle command."""

    def __init__(self):
        super().__init__('distance_controller')

        self.declare_parameter('threshold_cm', 50.0)
        self.declare_parameter('near_angle', 90)
        self.declare_parameter('far_angle', 0)

        self.threshold = float(
            self.get_parameter('threshold_cm').value
        )
        self.near_angle = int(
            self.get_parameter('near_angle').value
        )
        self.far_angle = int(
            self.get_parameter('far_angle').value
        )

        self.last_angle = None

        self.distance_sub = self.create_subscription(
            Float32,
            '/distance_cm',
            self.distance_callback,
            10
        )

        self.servo_pub = self.create_publisher(
            Int16,
            '/servo_angle',
            10
        )

        self.get_logger().info(
            f'Distance controller started; threshold={self.threshold:.1f} cm'
        )

    def distance_callback(self, msg):
        distance = msg.data

        if distance <= self.threshold:
            angle = self.near_angle
        else:
            angle = self.far_angle

        # Publish only when the requested position changes.
        if angle == self.last_angle:
            return

        command = Int16()
        command.data = angle
        self.servo_pub.publish(command)

        self.get_logger().info(
            f'Distance: {distance:.1f} cm -> Servo: {angle} deg'
        )

        self.last_angle = angle


def main(args=None):
    rclpy.init(args=args)
    node = DistanceController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
