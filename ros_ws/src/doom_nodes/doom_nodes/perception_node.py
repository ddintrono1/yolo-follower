import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from doom_interfaces.msg import CentroidCoords

from cv_bridge import CvBridge

from ultralytics import YOLO

class Detector(Node):

    def __init__(self):
        super().__init__('perceptor')

        self.model = YOLO("yolov8n.pt")

        self.bridge = CvBridge()

        self.subscriber_ = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.detect,
            10
        )

        self.publisher_ = self.create_publisher(
            CentroidCoords,
            '/centroid_coords',
            10
        )

        self.get_logger().info(f"Detection node ready \n")

    def detect(self, msg):

        # convert a sensor_msgs\Image message in a 
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # detect a person (class : 0) inside the camera image 
        results = self.model(cv_image, device="cuda", classes=[0], verbose=False)

        # extract bounding box coordinates (check if any)
        if len(results[0].boxes) > 0:

            [x_min, y_min, x_max, y_max] = results[0].boxes.xyxy[0]

            # compute centroid
            x_mean = int((x_min + x_max) / 2)
            y_mean = int((y_min + y_max) / 2)

            # publish centroid
            centroid = CentroidCoords()
            centroid.u = x_mean
            centroid.v = y_mean
            centroid.header = msg.header
            
            self.publisher_.publish(centroid)


def main(args=None):
    rclpy.init(args=args)
    node = Detector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
    






        
        

