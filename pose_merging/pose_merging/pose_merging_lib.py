from .pose_merging_includes import *

def node_init(self):

    # SUBSCRIBERS

    self.truth_sub = self.create_subscription(Odometry, '/iBot/ground_truth', self.truth_callback, 10)
    self.odom_sub = self.create_subscription(Odometry, '/iBot/noisy_odom', self.odom_callback, 10)
    self.matched_pose_sub = self.create_subscription(Odometry, '/iBot/matched_pose', self.matched_pose_callback, 10)
    self.match_status_sub = self.create_subscription(Bool, '/iBot/match_status', self.matched_status_callback, 10)

    # PUBLISHERS

    self.merged_pose_pub = self.create_publisher(Vector3, '/iBot/pose_merger/merged_pose', 10)

    # SERVICES

    self.save_pose_data_srv = self.create_service(Trigger, '/iBot/pose_merger/save_pose_data', self.save_pose_data_callback)

    # PUBLISHER TIMERS

    timer_period = 1
    self.merged_pose_timer = self.create_timer(timer_period, self.merged_pose_timer_callback)

    # EXTRA TIMERS

    self.plot_timer = self.create_timer(timer_period, self.plot_timer_callback)

#* CALLBACKS

#* SUBSCRIBER CALLBACKS

def truth_callback(self, data):
    global truth_pose, truth_array
    truth_pose = data
    truth_array[0].append(truth_pose.pose.pose.position.x)
    truth_array[1].append(truth_pose.pose.pose.position.y)
    truth_array[2].append(truth_pose.pose.pose.position.z)

def odom_callback(self, data):
    global ekf_pose
    ekf_pose = data
    ekf_array[0].append(ekf_pose.pose.pose.position.x)
    ekf_array[1].append(ekf_pose.pose.pose.position.y)
    ekf_array[2].append(ekf_pose.pose.pose.position.z)

def matched_pose_callback(self, data):
    global matched_pose
    matched_pose = data

def matched_status_callback(self, data):
    global matched_status
    matched_status = data

#* PUBLISHER CALLBACKS

def merged_pose_timer_callback(self):
    global merged_pose, truth_pose, matched_pose, X
    # if not(matched_pose.pose.pose.position.x == -1000 and matched_pose.pose.pose.position.y == -1000 and matched_pose.pose.pose.position.z == -1000):
    #     merged_pose.x = (((1-X)*matched_pose.pose.pose.position.x + X*ekf_pose.pose.pose.position.x))
    #     merged_pose.y = (((1-X)*matched_pose.pose.pose.position.y + X*ekf_pose.pose.pose.position.y))
    #     merged_pose.z = (((1-X)*matched_pose.pose.pose.position.z + X*ekf_pose.pose.pose.position.z))
    # else:
    #     merged_pose.x = ekf_pose.pose.pose.position.x
    #     merged_pose.y = ekf_pose.pose.pose.position.y
    #     merged_pose.z = ekf_pose.pose.pose.position.z

    merged_pose.x = matched_pose.pose.pose.position.x
    merged_pose.y = matched_pose.pose.pose.position.y
    merged_pose.z = matched_pose.pose.pose.position.z

    self.merged_pose_pub.publish(merged_pose)

    merged_array[0].append(merged_pose.x)
    merged_array[1].append(merged_pose.y)
    merged_array[2].append(merged_pose.z)

def plot_timer_callback(self):
    global truth_array, ekf_array, merged_array
    global truth_pose, ekf_pose, merged_pose

    print(ekf_pose.pose.pose.position)
    
    # dist_ekf = dist([ekf_pose.pose.pose.position.x,ekf_pose.pose.pose.position.y],[truth_pose.pose.pose.position.x,truth_pose.pose.pose.position.y])
    # dist_merged = dist([merged_pose.x,merged_pose.y],[truth_pose.pose.pose.position.x,truth_pose.pose.pose.position.y])

    # if dist_ekf < dist_merged: 
    #     print('ekf: ' + str(dist_ekf))
    # else:
    #     print('merged: ' + str(dist_merged))
    
    

def save_pose_data_callback(self, request, response):
    d = {
        # 'truth_pose_x': truth_array[0][:50],
        'truth_pose_y': truth_array[1][:50],
        'truth_pose_z': truth_array[2][:50],
        # 'ekf_pose_x': ekf_array[0][:50],
        'ekf_pose_y': ekf_array[1][:50],
        'ekf_pose_z': ekf_array[2][:50],
        # 'merged_pose_x': merged_array[0][:50],
        'merged_pose_y': merged_array[1][:50],
        'merged_pose_z': merged_array[2][:50],
        }
    benchmarks = pd.DataFrame(data=d)
    benchmarks.to_csv(benchmarks_path)

    response.success = True
    response.message = 'Pose data saved in: ' + benchmarks_path
    # self.get_logger().info('Pose Data Saved')

    return response
