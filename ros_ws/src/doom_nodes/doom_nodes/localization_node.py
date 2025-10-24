import rclpy
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import PointStamped
from doom_interfaces.msg import CentroidCoords

from message_filters import Subscriber, ApproximateTimeSynchronizer
import sensor_msgs_py.point_cloud2 as pc2

import numpy as np


class Localizer(Node):

    def __init__(self):
        super().__init__('localizer')

        self.sub_centroid = Subscriber(self, CentroidCoords, '/centroid_coords')
        self.sub_depth = Subscriber(self, PointCloud2, '/camera/depth/points')

        # Initialize approximate time synchonizer to synchronize the two different messages
        ats = ApproximateTimeSynchronizer(
            [self.sub_centroid, self.sub_depth],
            queue_size=10,
            slop=0.1
        )
        ats.registerCallback(self.localize)

        self.publisher_ = self.create_publisher(
            PointStamped,
            '/target_position_camera',
            10
        )

        self.get_logger().info(f"Localization node ready \n")

    def localize(self, msg_centroid, msg_depth):
        '''
        This function combines the informations from both the perception node and the depth camera 
        to indentify and publish the 3D position of the target in the environment 
        '''
        u = msg_centroid.u
        v = msg_centroid.v
        
        # If the 'error centroid' has been received, forward the 'error point', otherwise 
        # normally extract the depth point from the pointcloud
        if u < 0 or v < 0:
            x = 0.0
            y = 0.0
            z = -1.0
        else: 
            height = msg_depth.height
            width = msg_depth.width
            # The pointcloud has linear indexing
            index = v * width + u   
            points_array = pc2.read_points_numpy(msg_depth, field_names=("x", "y", "z"))
            x, y, z = points_array[index]

        msg = PointStamped()
        msg.point.x = float(x)
        msg.point.y = float(y)
        msg.point.z = float(z)
        msg.header = msg_depth.header

        self.publisher_.publish(msg)




def main(args=None):
    rclpy.init(args=args)
    node = Localizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
