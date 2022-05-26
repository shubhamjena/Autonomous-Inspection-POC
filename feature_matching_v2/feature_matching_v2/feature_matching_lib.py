from re import A
from .feature_matching_includes import *
from .image_matching import MatchImageHistogram

def node_init(self):
    self.cvBridge = CvBridge() # converting ros images to opencv data

    # Subscribers
    self.camera_image_sub = self.create_subscription(Image,'/iBot/camera/image',self.camera_image_callback,10)
    self.ibot_odom_sub = self.create_subscription(Odometry,'/iBot/odom',self.ibot_odom_callback,10)
    self.odom_sub = self.create_subscription(Odometry,'/odometry/filtered',self.odom_callback,10)

    #Publishers
    self.match_status_pub = self.create_publisher(Bool, '/iBot/feature_match_status', 10)
    self.match_position_pub = self.create_publisher(Vector3,'/iBot/feature_match_position', 10)
    self.filtered_image_pub = self.create_publisher(Image,'/iBot/filtered_image', 1)

    #Publisher Timers
    timer_period = 0.1
    self.match_status_timer = self.create_timer(timer_period, self.match_status_timer_callback)
    self.match_position_timer = self.create_timer(timer_period, self.match_position_timer_callback)
    self.filtered_image_timer = self.create_timer(0.1, self.filtered_image_timer_callback)

#* CALLBACKS

def camera_image_callback(self, data):
    global filtered_img, matched_pose
    camera_img = self.cvBridge.imgmsg_to_cv2(data)
    edges = cv2.Canny(camera_img, 50, 200, apertureSize=5)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = camera_img
    cv2.drawContours(contour_img, contours, -1, (255,0,0), 3)
    filtered_img = self.cvBridge.cv2_to_imgmsg(cvim=contour_img, encoding="rgb8")

    robot_coordinates = [
        ekf_output.pose.pose.position.x,
        ekf_output.pose.pose.position.y,
        0,
    ]

    count_pass = False
    length_pass = False
    if len(contours) > 3:
        count_pass = True

    max_contour = max(contours, key=len)
    if len(max_contour) > 100:
        length_pass = True
    
    if count_pass and length_pass:
        closest_coords, closest_name = MatchImageHistogram(camera_img, '', robot_coordinates)
        if closest_name == []:
            matched_pose.x = float(-1000)
            matched_pose.y = float(-1000)
            matched_pose.z = float(-1000)
            print('rejected pose due to distance > threshold')
        else:
            print(closest_coords + [closest_name])
            matched_pose.x = float(closest_coords[0])
            matched_pose.y = float(closest_coords[1])
            matched_pose.z = float(closest_coords[2])
    else:
        matched_pose.x = float(-1000)
        matched_pose.y = float(-1000)
        matched_pose.z = float(-1000)


def odom_callback(self, data):
    global ekf_output
    ekf_output = data

def ibot_odom_callback(self, data):
    global controller_output
    controller_output = data

def match_status_timer_callback(self):
    global match_status
    if not(matched_pose.x == -1000 and matched_pose.y == -1000 and matched_pose.z == -1000):
        match_status.data = True
    self.match_status_pub.publish(match_status)
    match_status.data = False

def match_position_timer_callback(self):
    global matched_pose
    if not(matched_pose.x == -1000 and matched_pose.y == -1000 and matched_pose.z == -1000):
        self.match_position_pub.publish(matched_pose)
    matched_pose.x = float(-1000)
    matched_pose.y = float(-1000)
    matched_pose.z = float(-1000)

def filtered_image_timer_callback(self):
    global filtered_img
    self.filtered_image_pub.publish(filtered_img)

#* FUNCTIONS