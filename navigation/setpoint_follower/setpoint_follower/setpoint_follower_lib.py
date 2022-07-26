from .setpoint_follower_includes import *

def node_init(self):

    # SUBSCRIBERS

    self.imu_subscriber = self.create_subscription(Imu, '/iBot/imu', self.imu_callback, 10)
    self.odom_subscriber = self.create_subscription(Odometry,'/iBot/odometry/filtered',self.odom_callback,1)
    self.estimated_pose_subscriber = self.create_subscription(Odometry,'/iBot/matched_pose',self.estimated_pose_callback,1)

    # PUBLISHERS

    self.velocity_publisher = self.create_publisher(Twist, '/iBot/cmd_vel', 10)

    # PUBLISHER TIMERS

    timer_period = 0.1
    self.velocity_timer = self.create_timer(timer_period, self.velocity_timer_callback)
    
    # EXTRA TIMERS

    self.follow_setpoint_timer = self.create_timer(timer_period, self.follow_setpoint_callback)
    

#* CALLBACKS

#* SUBSCRIBER CALLBACKS

def odom_callback(self, data):
    global ekf_output
    ekf_output = data

def estimated_pose_callback(self, data):
    global estimated_pose
    estimated_pose = data
    
def imu_callback(self, data):
    global imu, orientation, orientation_unit, X, correction_vector_bot_frame
    imu = data
    R = tf_transformations.quaternion_matrix([imu.orientation.x,imu.orientation.y,imu.orientation.z,imu.orientation.w])
    R_t = R.transpose()
    correction_vector = [
        current_setpoint[0] - ekf_output.pose.pose.position.x,
        current_setpoint[1] - ekf_output.pose.pose.position.y,
        current_setpoint[2] - estimated_pose.pose.pose.position.z
        # current_setpoint[2] - 0,
    ]
    correction_vector_bot_frame = np.matmul(R_t[0:3,0:3], correction_vector)
    correction_vector_bot_frame = unit_vector(correction_vector_bot_frame)

#* PUBLISHER CALLBACKS

def velocity_timer_callback(self):
    global correction_factor, twist

    ''' The Yaw of the bot is corrected according to yaw_correction and correction_factor '''
    twist.angular.z = yaw_correction*correction_factor

    self.velocity_publisher.publish(twist)

#* EXTRA CALLBACKS

def follow_setpoint_callback(self):
    global orientation_unit, n_hat, yaw_correction, correction_vector_bot_frame, twist, ekf_output, current_setpoint_number, setpoints_length, current_setpoint, estimated_pose

    ''' Change current setpoint if the bot is sufficiently close to the current setpoint '''

    if ((abs(ekf_output.pose.pose.position.x - current_setpoint[0]) <= 0.1) and (abs(ekf_output.pose.pose.position.y - current_setpoint[1]) <= 0.1) and (abs(estimated_pose.pose.pose.position.z - current_setpoint[2]) <= 0.05)):
        twist.angular.z = 0.0
        twist.linear.x = 0.0
        if current_setpoint_number < setpoints_length:
            current_setpoint_number += 1
            current_setpoint = setpoints[current_setpoint_number]
            print("setpoint changed to: ", current_setpoint)
        return

    ''' Get the projection of correction vector on the (xy plane) vector '''
    projected_vector = correction_vector_bot_frame -  np.dot(correction_vector_bot_frame, n_hat)*np.array(n_hat)

    ''' Make the vectors zero if very close to zero. To avoid unnecessary signs errors while calculating angle '''
    projected_vector = make_zero(projected_vector)
    cross_product = np.cross(projected_vector, X)
    correction_angle = angle_between(projected_vector, X)

    ''' Reject NaN correction angles '''
    if(correction_angle == np.nan):
        correction_angle = 0
    
    ''' Initialize Yaw '''
    yaw_correction = 1
    
    if abs(correction_angle) >= 0.05:
        ''' 
        Rotate the bot till correction angle < 0.05 radians
        ''' 
        yaw_correction = yaw_correction*abs(correction_angle) * -(np.sign(cross_product[2]))
        twist.linear.x = 0.0
    else:
        ''' 
        Move the bot forward with minute yaw corrections
        ''' 
        yaw_correction = yaw_correction*abs(correction_angle) * -(np.sign(cross_product[2]))
        twist.linear.x = 0.1

    '''
    Check if the bot is inverted or not,
    on the basis of its position wrt COM of the Cessna Plane (currently 6.5),
    and invert the yaw to rectify yaw direction whilst inverted
    '''
    if estimated_pose.pose.pose.position.z - 6.5 <= 0:
        yaw_correction = -yaw_correction

    print(correction_vector_bot_frame)
    # print(projected_vector)


#* Helper Functions

def unit_vector(vector):
    """ Returns the unit vector of the input vector.  """
    if vector[0] == 0 and vector[1] == 0 and vector[2] == 0:
        return vector
    else:
        return vector/np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -10.0, 10.0))

def make_zero(vector):
    ''' Makes the vector zero if it is close to zero '''
    for i in range(len(vector)):
        if abs(vector[i]) <= 0.05:
            vector[i] = 0
    return vector



