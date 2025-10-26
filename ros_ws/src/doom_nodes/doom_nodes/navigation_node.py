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
from action_msgs.msg import GoalStatus


class Navigator(Node):

    def __init__(self):
        super().__init__('navigator')

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Transform-related variables
        self.camera_frame = 'camera_rgb_frame'
        self.robot_frame = 'base_link'
        self.global_frame = 'map'
        self.transform_timeout = rclpy.duration.Duration(seconds=0.5)
        self.person_position_camera = None

        # Null point definition, utils
        self.null_point = PointStamped()
        self.null_point.point.x = 0.0
        self.null_point.point.y = 0.0
        self.null_point.point.z = 0.0
        
        # Node 'internal state'
        self.goal_in_progress = False
        self.current_goal_handle = None
        self.current_goal = None

        # Safety distance from the target
        self.stopping_distance = 0.75

        # Update tolerances
        self.distance_update_threshold = 0.05
        self.yaw_update_threshold = 0.05

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

        # Check if the target point has already been published
        if self.person_position_camera is None:
            return

        # Check if the 'error point' has been received, in this case stop the robot
        if self.person_position_camera.point.z == -1.0:
            self.get_logger().warn("Target lost. Stopping robot.")
            if self.goal_in_progress and self.current_goal_handle:
                self.current_goal_handle.cancel_goal_async()
                self.goal_in_progress = False
                self.current_goal_handle = None
                self.current_goal = None                
            return

        # Transform the target point from the robot camera frame to the global map frame
        try:
            t = self.tf_buffer.lookup_transform(
                self.global_frame,
                self.camera_frame,
                self.person_position_camera.header.stamp,
                timeout=self.transform_timeout
            )
            person_position = do_transform_point(self.person_position_camera, t)
        except TransformException as ex:
            return
        
        # Retrieve robot current position wrt the global map frame
        robot_position = self.get_robot_position(self.global_frame)
        if robot_position is None:
            self.get_logger().warn("Could not get robot position, skipping navigation.")
            return   

        # Compute the new goal, goal SLD distance
        self.next_goal, goal_distance = self.compute_goal(robot_position, person_position)

        # If the SLD to the goal is less than a threshold, just rotate towards the goal
        if goal_distance < self.stopping_distance:
            self.next_goal.pose.position = robot_position.point

        # Reset the goal if one goal was already up, otherwise simply set the goal
        if self.goal_in_progress:
            # Skip the goal reset if the new goal is similar to the old one
            if not self.are_goals_different(self.current_goal, self.next_goal):
                return
            # Cancel the previous goal
            cancel_future = self.current_goal_handle.cancel_goal_async()
            # Reset the goal as soon as it's cancelled using the callback 
            cancel_future.add_done_callback(self.goal_canceled_callback)
        else:
            self.send_goal(self.next_goal)

    def are_goals_different(self, old_goal, new_goal):
        '''
        This function checks if the given goals are significantly different, in terms of distance or angle
        '''
        # If one of the two goals does not exist, then the new goal of course is different
        if old_goal is None or new_goal is None:
            return True
        
        # Check linear distance between goals
        dist = math.hypot(
            new_goal.pose.position.x - old_goal.pose.position.x,
            new_goal.pose.position.y - old_goal.pose.position.y
            )
        if dist > self.distance_update_threshold:
            return True 

        # Check angular distance between goals
        old_yaw = self.quaternion_to_yaw(old_goal.pose.orientation)
        new_yaw = self.quaternion_to_yaw(new_goal.pose.orientation)
        yaw_diff = abs(self.normalize_angle(old_yaw - new_yaw))
        if yaw_diff > self.yaw_update_threshold:
            return True
        
        # If none of the previous conditions is satisfied, then the new goal is very close to the old one
        return False

    def get_robot_position(self, source_frame):
        '''
        This function retrieves the robot position wrt a specified frame
        '''
        try:
            t = self.tf_buffer.lookup_transform(
                source_frame,
                self.robot_frame,
                Time(),
                self.transform_timeout
            )
            # The transform uses the null point since the robot in its own frame is located of course in 
            # the null coordinates 
            self.null_point.header.frame_id = self.robot_frame
            self.null_point.header.stamp = Time().to_msg()
            robot_position = do_transform_point(self.null_point, t)
            return robot_position
        except TransformException as ex:
            return

    def compute_goal(self, robot_position, target_position):
        '''
        This function computes the goal pose and the distance based on the robot starting position
        and target position
        '''
        robot_x = robot_position.point.x
        robot_y = robot_position.point.y
        target_x = target_position.point.x
        target_y = target_position.point.y
        dx = target_x - robot_x
        dy = target_y - robot_y 

        goal_distance = math.hypot(dx, dy)

        yaw = math.atan2(dy, dx)
        q = self.yaw_to_quaternion(yaw)

        goal_pose = PoseStamped()
        goal_pose.pose.position.x = target_x
        goal_pose.pose.position.y = target_y
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation = q
        goal_pose.header.frame_id = self.global_frame
        goal_pose.header.stamp = self.get_clock().now().to_msg()

        return goal_pose, goal_distance        

    def save_point(self, msg):
        '''
        This function saves the received target point. It's the subscriber callback
        '''
        self.person_position_camera = msg

    def goal_canceled_callback(self, future):
        '''
        This function is called as soon as the goal is canceled, sending the new goal
        '''
        # If the goal has been successfully canceled, send the new_goal and reset the state,
        # otherwise simply reset the state 
        try:
            
            cancel_response = future.result()
            self.goal_in_progress = False
            self.current_goal_handle = None
            self.current_goal = None
            self.send_goal(self.next_goal)
        except:
            self.goal_in_progress = False
            self.current_goal_handle = None
            self.current_goal = None
 
    def send_goal(self, goal_pose):
        '''
        This function asynchronously sends a goal message, then it sets a callback to be executed
        when the nav2 server answers the call
        '''
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = goal_pose

        self.get_logger().info(f'Sending goal: {goal_pose.pose.position.x}, {goal_pose.pose.position.y}')

        self._action_client.wait_for_server()

        # Asynchronously send goal 
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)

        # Add callback to be executed when the goal request has been served
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        '''
        This function sets the flag and logs depending on whether or not the goal is accepted
        '''
        goal_handle = future.result()

        # If the goal has not been accepted, log and reset the internal state
        if not goal_handle.accepted:
            self.get_logger().warn('Goal rejected')
            self.goal_in_progress = False
            self.current_goal_handle = None
            self.current_goal = None
            return

        # If the goal has not been accepted, log and set the internal state
        self.get_logger().info('Goal accepted')
        self.goal_in_progress = True
        self.current_goal_handle = goal_handle
        self.current_goal = self.next_goal

        # Asynchronously ask for navigation results
        self._get_result_future = goal_handle.get_result_async()

        # Add callback to be executed when the results request has been served
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        '''
        This function resets the node internal state when the navigation finishes
        '''
        self.goal_in_progress = False
        self.current_goal_handle = None
        self.current_goal = None

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
    
    @staticmethod
    def quaternion_to_yaw(q):
        '''
        This function computes the yaw angle for robots moving on a plane, given the quaternion
        '''
        yaw = 2.0 * math.atan2(q.z, q.w)
        return yaw

    @staticmethod
    def normalize_angle(angle):
        '''
        This function normalizes an angle between -pi and +pi.
        For instance, in this way, 359° will be close to 1°
        '''
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle



        
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
