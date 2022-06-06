from requests import head
from .feature_matching_includes import *

def node_init(self):
    self.cvBridge = CvBridge()

    # Subscribers
    
    self.camera_image_sub = self.create_subscription(Image,'/iBot/camera/image',self.camera_image_callback,1)
    self.ibot_odom_sub = self.create_subscription(Odometry,'/iBot/odom',self.ibot_odom_callback,1)
    self.odom_sub = self.create_subscription(Odometry,'/iBot/odometry/filtered',self.odom_callback,1)
    self.velocity_sub = self.create_subscription(Twist,'/iBot/cmd_vel',self.velocity_callback,1)
    self.imu_sub = self.create_subscription(Imu,'/iBot/imu',self.imu_callback,1)

    #Publishers

    self.match_status_pub = self.create_publisher(Bool, '/iBot/match_status', 1)
    self.match_position_pub = self.create_publisher(Odometry,'/iBot/matched_pose', 1)
    self.filtered_image_pub = self.create_publisher(Image,'/iBot/filtered_image', 1)

    #Publisher Timers

    self.match_status_timer = self.create_timer(timer_period, self.match_status_timer_callback)
    self.match_position_timer = self.create_timer(timer_period, self.match_position_timer_callback)
    self.filtered_image_timer = self.create_timer(timer_period, self.filtered_image_timer_callback)

#* CALLBACKS

#* SUBSCRIBER CALLBACKS

def camera_image_callback(self, data):
    global filtered_img, matched_pose, estimated_z, fallback, robot_coordinates, temp_z
    camera_img = self.cvBridge.imgmsg_to_cv2(data)
    edges = cv2.Canny(camera_img, 50, 200, apertureSize=5)

    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = camera_img
    cv2.drawContours(contour_img, contours, -1, (255,0,0), 3)
    filtered_img = self.cvBridge.cv2_to_imgmsg(cvim=contour_img, encoding="rgb8")

    # robot_coordinates = [
    #     ekf_output.pose.pose.position.x,
    #     ekf_output.pose.pose.position.y,
    #     estimated_z.data,
    # ]

    angles = tf_transformations.euler_from_quaternion([imu.orientation.x,imu.orientation.y,imu.orientation.z,imu.orientation.w], axes='szyx')
    R = tf_transformations.quaternion_matrix([imu.orientation.x,imu.orientation.y,imu.orientation.z,imu.orientation.w])
    X = [1, 0, 0]
    V = np.matmul(R[0:3, 0:3], X)

    closest_coords, closest_name, temp = MatchImageHistogram(camera_img, '', robot_coordinates)

    # print('estimated_z: ' + str(estimated_z.data))
    # print('ekf_y: ' + str(ekf_output.pose.pose.position.y))
    if velocity.linear.x != 0:
        # heading = (angles[2]/abs(angles[2])) * (velocity.linear.x/abs(velocity.linear.x))
        heading = V[2]/abs(V[2])
    else:
        heading = 0

    if not fallback:
        distance = 100000000
        # temp_z = estimated_z.data
        robot_coordinates = [
            ekf_output.pose.pose.position.x,
            ekf_output.pose.pose.position.y,
            estimated_z.data,
        ]
        df = dataset_coordinates.iloc[(dataset_coordinates['Y']-ekf_output.pose.pose.position.y).abs().argsort()[:2]]
        # print(df)
        for index, row in df.iterrows():
            if heading > 0:
                if (row['Z'] + CESSNA_HEIGHT) > robot_coordinates[2]:
                    temp_dist = math.dist([row['X'],row['Y'],row['Z'] + CESSNA_HEIGHT], robot_coordinates)
                    if temp_dist < distance:
                        distance = temp_dist
                        estimated_z.data = row['Z'] + CESSNA_HEIGHT
                else:
                    continue
            elif heading < 0:
                if (row['Z'] + CESSNA_HEIGHT) < robot_coordinates[2]:
                    temp_dist = math.dist([row['X'],row['Y'],row['Z'] + CESSNA_HEIGHT], robot_coordinates)
                    if temp_dist < distance:
                        distance = temp_dist
                        estimated_z.data = row['Z'] + CESSNA_HEIGHT
                else:
                    continue

        if abs(temp_z - estimated_z.data) > 0.5:
            estimated_z.data = temp_z
        else:
            temp_z = estimated_z.data

        robot_coordinates = [
            ekf_output.pose.pose.position.x,
            ekf_output.pose.pose.position.y,
            estimated_z.data,
        ]
        closest_coords, closest_name, temp = MatchImageHistogram(camera_img, '', robot_coordinates)
        matched_pose.x = robot_coordinates[0]
        matched_pose.y = robot_coordinates[1]
        matched_pose.z = robot_coordinates[2]

    # if fallback:
    #     distance = 100000000
    #     temp_z = estimated_z.data
    #     robot_coordinates = [
    #         ekf_output.pose.pose.position.x,
    #         ekf_output.pose.pose.position.y,
    #         estimated_z.data,
    #     ]
    #     df = dataset_coordinates.iloc[(dataset_coordinates['Y']-ekf_output.pose.pose.position.y).abs().argsort()[:2]]
    #     # print(df)
    #     for index, row in df.iterrows():
    #         # print(row['Y'], type(row['Y']))
    #         temp_dist = math.dist([row['X'],row['Y'],row['Z'] + CESSNA_HEIGHT], robot_coordinates)
    #         if temp_dist < distance:
    #             distance = temp_dist
    #             estimated_z.data = row['Z'] + CESSNA_HEIGHT

    #     robot_coordinates = [
    #         ekf_output.pose.pose.position.x,
    #         ekf_output.pose.pose.position.y,
    #         estimated_z.data,
    #     ]
    #     closest_coords, closest_name, temp = MatchImageHistogram(camera_img, '', robot_coordinates)
    #     if(abs(temp - estimated_z.data) < 0.05):
    #         estimated_z.data = temp
    #         fallback = False
    #         print('fallback off')
    # else:
    #     robot_coordinates = [
    #         ekf_output.pose.pose.position.x,
    #         ekf_output.pose.pose.position.y,
    #         estimated_z.data,
    #     ]
        
    #     closest_coords, closest_name, temp = MatchImageHistogram(camera_img, '', robot_coordinates)

    #     if ((abs(temp - estimated_z.data) < 0.05) or (abs(temp - estimated_z.data) > 0.1)) and (abs(velocity.linear.x) > 0.001):
    #         fallback = True
    #         print('fallback on')

    #         distance = 100000000
    #         temp_z = estimated_z.data
    #         robot_coordinates = [
    #             ekf_output.pose.pose.position.x,
    #             ekf_output.pose.pose.position.y,
    #             estimated_z.data,
    #         ]
    #         df = dataset_coordinates.iloc[(dataset_coordinates['Y']-ekf_output.pose.pose.position.y).abs().argsort()[:2]]
    #         # print(df)
    #         for index, row in df.iterrows():
    #             # print(row['Y'], type(row['Y']))
    #             temp_dist = math.dist([row['X'],row['Y'],row['Z'] + CESSNA_HEIGHT], robot_coordinates)
    #             if temp_dist < distance:
    #                 distance = temp_dist
    #                 estimated_z.data = row['Z'] + CESSNA_HEIGHT
    #     else:
    #         estimated_z.data = temp



    # print('estimated z: ' + str(estimated_z))

    # if closest_name == []:
    #     # matched_pose.x = float(-1000)
    #     # matched_pose.y = float(-1000)
    #     # matched_pose.z = float(-1000)
    #     print('rejected pose due to distance > threshold')
    # else:
    #     print(closest_coords + [closest_name])
    #     # matched_pose.x = float(closest_coords[0])
    #     # matched_pose.y = float(closest_coords[1])
    #     # matched_pose.z = float(closest_coords[2])

def odom_callback(self, data):
    global ekf_output
    ekf_output = data

def ibot_odom_callback(self, data):
    global controller_output
    controller_output = data

def velocity_callback(self, data):
    global velocity
    velocity = data
    
def imu_callback(self, data):
    global imu
    imu = data

#* PUBLISHER CALLBACKS

def match_status_timer_callback(self):
    global match_status
    if not(matched_pose.x == -1000 and matched_pose.y == -1000 and matched_pose.z == -1000):
        match_status.data = True
    self.match_status_pub.publish(match_status)
    match_status.data = False

def match_position_timer_callback(self):
    global matched_pose
    temp = Odometry()
    temp.pose.pose.position.x = matched_pose.x
    temp.pose.pose.position.y = matched_pose.y
    temp.pose.pose.position.z = matched_pose.z
    temp.child_frame_id = 'robot_footprint'
    temp.header.frame_id = 'odom'
    self.match_position_pub.publish(temp)

def filtered_image_timer_callback(self):
    global filtered_img
    self.filtered_image_pub.publish(filtered_img)


#* FUNCTIONS