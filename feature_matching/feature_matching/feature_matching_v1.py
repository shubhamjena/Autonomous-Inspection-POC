# structure for feature node communication. subscriber and publisher communication established.
import rclpy 
import cv2 
from rclpy.node import Node 
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image
from geometry_msgs.msg import Vector3
from std_msgs.msg import Bool # can give string if needed
from std_msgs.msg import Float32


class feature_match(Node):
  def __init__(self):
    super().__init__('feature_matcher')
    self.subscriber = self.create_subscription(Image,'/iBot/camera/image',self.process_data,10)
    self.bridge = CvBridge() # converting ros images to opencv data
    
    # topic 
    self.publisher_position = self.create_publisher(Vector3, '/iBot/feature_match_position', 10)
    self.publisher_status = self.create_publisher(Bool, '/iBot/feature_match_status', 10)
    self.publisher_confidence = self.create_publisher(Float32, '/iBot/feature_match_confidence', 10)
    
    timer_period = 0.5  # seconds
    self.timer = self.create_timer(timer_period, self.timer_callback)
   
  def process_data(self, data): 
    frame = self.bridge.imgmsg_to_cv2(data) # performing conversion
    cv2.imshow("output", frame) # displaying what is being recorded 
    cv2.imwrite('/home/nbeena/image_ws/src/Autonomous-Inspection-POC/images/image.jpg', frame)
    cv2.waitKey(1) # will save video until it is interrupted
    
  def timer_callback(self):
        feature_position = Vector3()
        feature_position.x = 0.5
        feature_position.y = 0.5
        feature_position.z = 0.3
        feature_status=Bool()
        feature_status.data=True
        feature_confidence=Float32()
        feature_confidence.data=0.75
        
        # send information on topic
        self.publisher_position.publish(feature_position)
        self.publisher_status.publish(feature_status)
        self.publisher_confidence.publish(feature_confidence)
        self.get_logger().info("Feature match="+ str(feature_status.data)+ ", confidence="+str(int(feature_confidence.data*100))+"%"+" at : x = %0.2f, y = %0.2f, z=%0.2f" % (feature_position.x, feature_position.y, feature_position.z))
        
  
def main(args=None):
  rclpy.init(args=args)
  feature = feature_match()
  rclpy.spin(feature)
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
