import rclpy
from rclpy.node import Node

import argparse

import math

from geometry_msgs.msg import PoseWithCovarianceStamped

from nav_msgs.msg import OccupancyGrid


class InitStatePub(Node):

    def __init__(self):
        super().__init__('initial_state_publisher')

        self.declare_parameter('x', 0.0)
        self.declare_parameter('y', 0.0)
        self.declare_parameter('yaw', 0.0)

        self.x = self.get_parameter('x').value
        self.y = self.get_parameter('y').value
        self.yaw = self.get_parameter('yaw').value        
        
        self.publisher_ = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        # publish position only when nav2 is ready
        self.subscriber_ = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.publish_pose,
            10
        )

        self.get_logger().info(f'Waiting for Nav2 to be ready...')

    def publish_pose(self, placeholder_msg):

        self.destroy_subscription(self.subscriber_)

        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.orientation.x = 0.0
        msg.pose.pose.orientation.y = 0.0
        msg.pose.pose.orientation.z = math.sin(self.yaw/2.0)
        msg.pose.pose.orientation.w = math.cos(self.yaw/2.0)
        self.publisher_.publish(msg)

        self.get_logger().info(f'Initial pose published')

        self.timer = self.create_timer(2.0, self.shutdown_node)

    def shutdown_node(self):

        self.get_logger().info(f'Mission accomplished, destroying node')
        
        self.destroy_node()
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    node = InitStatePub()    
    rclpy.spin(node)

if __name__ == '__main__':

    main()
