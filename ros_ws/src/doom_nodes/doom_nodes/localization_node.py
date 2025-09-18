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

        # approximate time synchonizer initialization
        ats = ApproximateTimeSynchronizer(
            [self.sub_centroid, self.sub_depth],
            queue_size=10,
            slop=5
        )
        ats.registerCallback(self.localize)

        self.publisher_ = self.create_publisher(
            PointStamped,
            '/target_position_camera',
            10
        )

        self.get_logger().info(f"Localization node ready \n")

    def localize(self, msg_centroid, msg_depth):

        u_depth = msg_centroid.u
        v_depth = msg_centroid.v

        height = msg_depth.height
        width = msg_depth.width

        # indice lineare nella PointCloud2
        index = v_depth * width + u_depth

        # leggere tutti i punti come array
        points = list(pc2.read_points(msg_depth, field_names=["x","y","z"]))

        # estrarre il punto desiderato
        x, y, z = points[index]

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
