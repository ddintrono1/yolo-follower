import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
from rclpy.action import ActionClient

import math

from geometry_msgs.msg import PointStamped, PoseStamped, Quaternion
from tf2_geometry_msgs import PointStamped

from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from tf2_ros import TransformException

from nav2_msgs.action import NavigateToPose


class Navigator(Node):

    def __init__(self):
        super().__init__('navigator')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.source_frame = 'camera_rgb_frame'
        self.target_frame = 'map'

        self.subscriber_ = self.create_subscription(
            PointStamped,
            '/target_position_camera',
            self.transform,
            10
        )

        self.already_triggered_flag = False         # debug

        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        #self.timer = self.create_timer(1.0, self.navigate)          # debug

        self.get_logger().info(f"Navigator node ready \n")         
             
    
    def transform(self, msg):
        # this function transforms the target coordinates from the camera frame to the global frame

        point_camera = msg

        try:
            self.person_global = self.tf_buffer.transform(point_camera, self.target_frame)                     
        except TransformException as ex:
            self.get_logger().info(
                f'Could not transform {self.source_frame} to {self.target_frame}: {ex}')
            return
        self.navigate()

    def navigate(self):

        if not hasattr(self, 'person_global'):
            return

        if self.already_triggered_flag:     # debug
            return

        self.already_triggered_flag = True  # debug

        self.get_logger().info(f"already_triggered_flag is now TRUE")

        robot_position_global = self.get_robot_position('map')
        goal_pose_global = self.compute_pose(robot_position_global, self.person_global)

        self.send_goal(goal_pose_global)


    def send_goal(self, goal_pose):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.get_logger().info(f'Sending goal: {goal_pose.pose.position.x}, {goal_pose.pose.position.y}')

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warn('Goal rejected')
            return
        self.get_logger().info('Goal accepted')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Navigation finished with result: {result}')

    def get_robot_position(self, source):
        # this function retrieves the robot position wrt a specified source frame
        robot_position = PointStamped()

        t = self.tf_buffer.lookup_transform(source, 'base_link', Time())
        robot_position.point.x = t.transform.translation.x
        robot_position.point.y = t.transform.translation.y
        robot_position.point.z = t.transform.translation.z #prova

        return robot_position

    def compute_pose(self, source_position, target_position):
        goal_pose = PoseStamped()
        q = Quaternion()

        source_x = source_position.point.x
        source_y = source_position.point.y
        target_x = target_position.point.x
        target_y = target_position.point.y

        dx = target_x - source_x
        dy = target_y - source_y

        d = math.sqrt(dx**2 + dy**2)
        
        scale = (d-0.5) / d

        x_goal = source_x + dx * scale
        y_goal = source_y + dy * scale    

        yaw = math.atan2(dy, dx)

        q.w = math.cos(yaw / 2.0)
        q.z = math.sin(yaw / 2.0)
        q.x = 0.0
        q.y = 0.0

        goal_pose.pose.position.x = x_goal
        goal_pose.pose.position.y = y_goal
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation = q

        goal_pose.header.frame_id = "map"
        goal_pose.header.stamp = self.get_clock().now().to_msg()

        return goal_pose


def main(args=None):            
    rclpy.init(args=args)
    node = Navigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()



    





