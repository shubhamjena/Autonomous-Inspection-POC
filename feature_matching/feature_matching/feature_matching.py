
import rclpy
import cv2
import numpy as np
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import Bool # can give string if needed
from pandas import read_csv

DATABASE='~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/DATABASE_test/'
CAMERA_IMAGES='~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/CAMERA_IMAGES/'
FEATURE_MATCHES='~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/FEATURE_MATCHES/'


DATABASE_coordinates='~/ros2/airbus_ws/src/Autonomous-Inspection-POC/feature_matching/DATABASE_coordinates_test.csv'
matches_publisher=[]
B_feature_match=0

class feature_match(Node):
  def __init__(self):
    super().__init__('feature_matcher')
    self.subscriber = self.create_subscription(Image,'/iBot/camera/image',self.process_data,10)
    self.bridge = CvBridge() # converting ros images to opencv data

    # topic publisher
    #self.publisher_position = self.create_publisher(Vector3, '/iBot/feature_match_position', 10)
    self.publisher_status = self.create_publisher(Bool, '/iBot/feature_match_status', 10)
    self.publisher_position = self.create_publisher(Float32MultiArray,'/iBot/feature_match_position', 10)


    timer_period = 0.5  # seconds
    self.timer = self.create_timer(timer_period, self.timer_callback)

  def process_data(self, data):
    self.get_logger().info("comparing image with database")

    camera_image = self.bridge.imgmsg_to_cv2(data) # performing conversion
    #camera_image=cv2.imread(CAMERA_IMAGES+'Cessna-0012.jpg') # only for demonstration

    # Check camera image for feature
    grayImage = cv2.cvtColor(camera_image, cv2.COLOR_BGR2GRAY)
    (thresh, bwImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    B_feature = bool(np.sum(bwImage)) or 1    # if sum is 0, the image has no features, remove 'or1'

    # Read database for figure name and coordinates
    df = read_csv(DATABASE_coordinates)
    coordinates_data=df.values # column 1: image ID
    global matches_publisher, B_feature_match
    matches_publisher=[]
    B_feature_match=0
    n_db_matches=0   # number of coordinates in database that match features
    n1=0
    if B_feature:
        for i in coordinates_data[:,0]:
            self.get_logger().info("reading image:"+str(i))
            database_image=cv2.imread(DATABASE+i+'.jpg')

            # to be replaces with Charan's code
            sift = cv2.xfeatures2d.SIFT_create()
            kp_1, desc_1 = sift.detectAndCompute(database_image, None)
            kp_2, desc_2 = sift.detectAndCompute(camera_image, None)
            FLANN_INDEX_KDTREE = 0
            index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
            search_params = dict(checks=50)
            flann = cv2.FlannBasedMatcher(index_params, search_params)
            matches = flann.knnMatch(desc_1, desc_2, k=2)
            good_points = []
            for m, n in matches:
                if m.distance < 0.6 *n.distance:
                    good_points.append(m)

            # Define how similar they are
            number_keypoints = 0
            if len(kp_1) <= len(kp_2):
                number_keypoints = len(kp_1)
            else:
                number_keypoints = len(kp_2)

            # % of match calculation
            if number_keypoints!= 0:
                percentage_match=len(good_points) / number_keypoints * 100
            else:
                percentage_match=0



            if len(good_points)>0:
                B_feature_match=1
                n_db_matches=n_db_matches+1
                matches_publisher.append(list(coordinates_data[n1,1:4])+list([percentage_match]))
                self.get_logger().info(str(matches_publisher))

                # save features matched figure
                result = cv2.drawMatches(database_image, kp_1, camera_image, kp_2, good_points, None)
                cv2.imwrite(FEATURE_MATCHES+i+".jpg", result)
            n1=n1+1

    while n_db_matches<4:
        matches_publisher.append([7777.0, 7777.0, 7777.0, 0])
        n_db_matches=n_db_matches+1

    matches_publisher=np.array(matches_publisher)
    matches_publisher=matches_publisher[np.argsort(-1*matches_publisher[:,3])] # sort with max % on top of array
    matches_publisher=matches_publisher[0:4,:].reshape(1,16).tolist()[0]
    self.get_logger().info(str(matches_publisher))
    cv2.waitKey(1)

  def timer_callback(self):
        global matches_publisher, B_feature_match
        feature_status=Bool()
        feature_status.data=bool(B_feature_match)

        mat = Float32MultiArray()
        #d=[1.2354567, 99.7890, 67.654236, 0.82, 67.875, 90.6543, 76.5689, 0.55, 65.3452, 45.873, 67.8956, 0.53]

        mat.data=matches_publisher
        mat.layout.data_offset = 0

        # create two dimensions in the dim array
        mat.layout.dim = [MultiArrayDimension(), MultiArrayDimension()]

        # dim[0] is the vertical dimension of your matrix
        mat.layout.dim[0].label = "xyz_match%"
        mat.layout.dim[0].size = 4
        mat.layout.dim[0].stride = 16
        # dim[1] is the horizontal dimension of your matrix
        mat.layout.dim[1].label = "top_4_matches"
        mat.layout.dim[1].size = 4
        mat.layout.dim[1].stride = 4

        # send information on topic
        self.publisher_position.publish(mat)
        self.publisher_status.publish(feature_status)
        #self.get_logger().info(str(mat.data))
        self.get_logger().info("Feature match="+ str(feature_status.data)+ ", coords="+str(mat.data))

def main(args=None):
  rclpy.init(args=args)
  feature = feature_match()
  rclpy.spin(feature)
  rclpy.shutdown()

if __name__ == '__main__':
  main()
