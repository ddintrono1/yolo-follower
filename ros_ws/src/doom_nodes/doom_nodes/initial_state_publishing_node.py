import rclpy
from rclpy.node import Node

import math

from geometry_msgs.msg import PoseWithCovarianceStamped, Quaternion

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

        # The callback will be triggered only when nav2 is ready, since only in this case
        # messages arrive on the /map topic
        self.subscriber_ = self.create_subscription(
            OccupancyGrid,
            '/map',
            self.publish_pose,
            10
        )

        self.get_logger().info(f'Waiting for Nav2 to be ready...')

    def publish_pose(self, placeholder_msg):
        '''
        This function publishes the initial pose based on the received parameters, 
        then calls a timer which triggers the node destruction procedure
        '''
        # Destroy subscriber to avoid running again this callback
        self.destroy_subscription(self.subscriber_)

        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        q = self.yaw_to_quaternion(self.yaw)
        msg.pose.pose.orientation = q

        self.publisher_.publish(msg)

        self.get_logger().info(f'Initial pose published')

        self.timer = self.create_timer(2.0, self.shutdown_node)

    def shutdown_node(self):

        self.get_logger().info(f'Mission accomplished, destroying node')
        
        self.destroy_node()
        rclpy.shutdown()

    @staticmethod
    def yaw_to_quaternion(yaw):
        '''
        This function computes the quaternion for robots moving on a plane, given the yaw angle
        '''
        q = Quaternion()
        q.w = math.cos(yaw / 2.0)
        q.z = math.sin(yaw / 2.0)
        q.x = 0.0
        q.y = 0.0
        return q




def main(args=None):
    rclpy.init(args=args)
    node = InitStatePub()    
    rclpy.spin(node)


if __name__ == '__main__':

    main()
