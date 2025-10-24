import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from doom_interfaces.msg import CentroidCoords

from cv_bridge import CvBridge

from ultralytics import YOLO


class Detector(Node):

    def __init__(self):
        super().__init__('perceptor')

        self.model = YOLO("yolov8m.pt")

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
        '''
        This function runs the YOLO model on the camera image to compute the person bounding box,
        then identifies and publishes the person pixel centroid
        '''
        # Convert a sensor_msgs\Image message in a format that can be used by the YOLO model
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        # Detect a person (class : 0) inside the camera image, use gpu
        results = self.model(cv_image, device="cuda", classes=[0], verbose=False)

        # Check that a person has actually been detected, otherwise publish the 'error centroid'
        if len(results[0].boxes) > 0:
            [x_min, y_min, x_max, y_max] = results[0].boxes.xyxy[0]

            # Compute centroid (top 25% to avoid targeting the void space between the legs)
            x_centroid = int((x_min + x_max) / 2)
            y_centroid = int(y_min + (y_max-y_min) * 0.25)

            centroid = CentroidCoords()
            centroid.u = x_centroid
            centroid.v = y_centroid
            centroid.header = msg.header    
        else: 
            centroid = CentroidCoords()
            centroid.u = -1
            centroid.v = -1
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
