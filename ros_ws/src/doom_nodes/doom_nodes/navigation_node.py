import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
from rclpy.action import ActionClient

import math

from geometry_msgs.msg import PointStamped, PoseStamped, Quaternion
from tf2_geometry_msgs.tf2_geometry_msgs import do_transform_point

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
        self.transform_timeout = rclpy.duration.Duration(seconds=0.5)
        self.point_camera = None

        # Null point definition, utils
        self.null_point = PointStamped()
        self.null_point.point.x = 0.0
        self.null_point.point.y = 0.0
        self.null_point.point.z = 0.0

        self.goal_in_progress = False       # flag to verify if one goal following is in progress
        self.current_goal_handle = None        
        self.stopping_distance = 0.5

        self.subscriber_ = self.create_subscription(
            PointStamped,
            '/target_position_camera',
            self.save_point,             
            10
        )

        self._action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        self.timer = self.create_timer(1.0, self.navigate)

        self.get_logger().info(f"Navigator node ready \n")         


    def navigate(self):

        # Check if the target point has already been published CONSIDERA EVENTUALMENTE DI INSERIRLO NEL COSTRUTTORE
        if self.point_camera is None:
            self.get_logger().info(f'Camera found no point')
            return

        # Check if the 'error point' has been received, in this case stop the robot
        if self.point_camera.point.z == -1.0:
            self.get_logger().warn("Target lost. Stopping robot.")
            if self.goal_in_progress and self.current_goal_handle:
                self.current_goal_handle.cancel_goal_async()
                self.goal_in_progress = False
                self.current_goal_handle = None                
            return

        # Transform the target point from the robot camera frame to the global frame
        try:
            t = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                self.point_camera.header.stamp,
                timeout=self.transform_timeout
            )
            person_global = do_transform_point(self.point_camera, t)
        except TransformException as ex:
            self.get_logger().warn(f"Lookup_transform failed: {ex}")
            return
        
        # Compute the new goal pose (robot position is useful to make yaw angle aim to the target)
        robot_position_global = self.get_robot_position('map')
        if robot_position_global is None:
             self.get_logger().warn("Could not get robot position, skipping navigation.")
             return
             
        self.goal_pose_global, goal_distance = self.compute_pose(robot_position_global, person_global)

        # If the SLD to the goal is less than a threshold, stop the robot and just rotate towards the goal
        if goal_distance < self.stopping_distance:
            self.get_logger().info(f'Target is close enough. Rotating the robot towards the goal.')
            self.goal_pose_global.pose.position = robot_position_global.point

        # Reset the goal if one goal was already up, otherwise simply set the goal
        if self.goal_in_progress:
            # Cancel the previous goal
            self.get_logger().info("Cancelling previous goal...")
            cancel_future = self.current_goal_handle.cancel_goal_async()
            # Reset the goal as soon as it's cancelled
            cancel_future.add_done_callback(
                lambda future: self.send_goal(self.goal_pose_global)
            )
        else:
            self.send_goal(self.goal_pose_global)
            

    def get_robot_position(self, source_frame):
        '''
        This function retrieves the robot position wrt a specified source frame
        '''
        self.null_point.header.frame_id = 'base_link'
        self.null_point.header.stamp = Time().to_msg()

        try:
            t = self.tf_buffer.lookup_transform(
                source_frame,
                'base_link',
                Time(),
                self.transform_timeout
            )
            robot_position = do_transform_point(self.null_point, t)
            return robot_position
        except TransformException as ex:
            self.get_logger().warn(f"lookup_transform failed: {ex}")
            return

    def compute_pose(self, source_position, target_position):
        '''
        This function computes the goal pose based on the robot starting position and target position
        '''
        goal_pose = PoseStamped()
        q = Quaternion()

        source_x = source_position.point.x
        source_y = source_position.point.y
        target_x = target_position.point.x
        target_y = target_position.point.y

        # Compute yaw angle which makes the robot point to the target, instanciate quaternion
        dx = target_x - source_x
        dy = target_y - source_y 
        goal_distance = math.hypot(dx, dy)
        yaw = math.atan2(dy, dx)
        q.w = math.cos(yaw / 2.0)
        q.z = math.sin(yaw / 2.0)
        q.x = 0.0
        q.y = 0.0

        goal_pose.pose.position.x = target_x
        goal_pose.pose.position.y = target_y
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation = q

        goal_pose.header.frame_id = "map"
        goal_pose.header.stamp = self.get_clock().now().to_msg()

        return goal_pose, goal_distance        

    def save_point(self, msg):
        '''
        This saves the received target point 
        '''
        self.point_camera = msg
        

    def send_goal(self, goal_pose):
        '''
        This function asynchronously sends a goal message, then it sets a callback to be executed
        when the nav2 server answers the call
        '''
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.get_logger().info(f'Sending goal: {goal_pose.pose.position.x}, {goal_pose.pose.position.y}')

        self._action_client.wait_for_server()

        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        # The following callback will be executed then the goal is forwarded to the action server
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        '''
        This function sets the flag and logs depending on whether or not the goal is accepted
        '''
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().warn('Goal rejected')
            self.goal_in_progress = False
            self.current_goal_handle = None
            return

        self.get_logger().info('Goal accepted')

        self.goal_in_progress = True
        self.current_goal_handle = goal_handle

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        '''
        This function sets the flag and logs depending on the navigation results
        '''
        result = future.result().result
        self.get_logger().info(f'Navigation finished with result: {result}')
        self.goal_in_progress = False
        self.current_goal_handle = None


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
