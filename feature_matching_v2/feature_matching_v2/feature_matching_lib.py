from .feature_matching_includes import *

def node_init(self):
    self.cvBridge = CvBridge() # converting ros images to opencv data

    # Subscribers
    self.camera_image_sub = self.create_subscription(Image,'/iBot/camera/image',self.camera_image_callback,10)
    self.ibot_odom_sub = self.create_subscription(Odometry,'/iBot/odom',self.ibot_odom_callback,10)
    self.odom_sub = self.create_subscription(Odometry,'/odometry/filtered',self.odom_callback,10)

    #Publishers
    self.match_status_pub = self.create_publisher(Bool, '/iBot/feature_match_status', 10)
    self.match_position_pub = self.create_publisher(Float32MultiArray,'/iBot/feature_match_position', 10)
    self.filtered_image_pub = self.create_publisher(Image,'/iBot/filtered_image', 1)

    #Publisher Timers
    timer_period = 0.5  # seconds
    self.match_status_timer = self.create_timer(timer_period, self.match_status_timer_callback)
    self.match_position_timer = self.create_timer(timer_period, self.match_position_timer_callback)
    self.filtered_image_timer = self.create_timer(0.1, self.filtered_image_timer_callback)


def camera_image_callback(self, data):
    # self.get_logger().info("camera image callback")
    global filtered_image
    camera_image = self.cvBridge.imgmsg_to_cv2(data)
    edges = cv2.Canny(camera_image,100,200)
    filtered_image = self.cvBridge.cv2_to_imgmsg(cvim=edges)

def odom_callback(self, data):
    a = 1
    # self.get_logger().info("odom callback")
    print("Odom Callback")
    print(data.pose.pose.position)
    # print('\n')

def ibot_odom_callback(self, data):
    a = 1
    # self.get_logger().info("ibot odom callback")
    # print("iBot odom Callback")
    # print(data.pose.pose.position)
    # print('\n')

def match_status_timer_callback(self):
    global B_feature_match
    feature_status=Bool()
    feature_status.data=bool(B_feature_match)

    self.match_status_pub.publish(feature_status)

    # self.get_logger().info("Feature match status : "+ str(feature_status.data))

def match_position_timer_callback(self):
    global matches_msg

    mat = Float32MultiArray()

    mat.data=matches_msg
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
    self.match_position_pub.publish(mat)
    # self.get_logger().info("Feature match coordinates : " + str(mat.data))

def filtered_image_timer_callback(self):
    global filtered_image
    self.filtered_image_pub.publish(filtered_image)