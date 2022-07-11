from .trajectory_follower_includes import *

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

    self.correct_traj_timer = self.create_timer(timer_period, self.correct_traj_callback)
    

#* CALLBACKS

#* SUBSCRIBER CALLBACKS

def odom_callback(self, data):
    global ekf_output
    ekf_output = data

def estimated_pose_callback(self, data):
    global estimated_pose
    estimated_pose = data
    
def imu_callback(self, data):
    global imu, orientation, orientation_unit
    imu = data
    R = tf_transformations.quaternion_matrix([imu.orientation.x,imu.orientation.y,imu.orientation.z,imu.orientation.w])
    X = [1, 0, 0]
    orientation = np.matmul(R[0:3, 0:3], X)
    orientation_unit = orientation/np.linalg.norm(orientation)

#* PUBLISHER CALLBACKS

def velocity_timer_callback(self):
    twist = Twist()
    twist.linear.x = +0.1
    twist.angular.z = yaw_correction*5
    self.velocity_publisher.publish(twist)

#* EXTRA CALLBACKS

def correct_traj_callback(self):
    global orientation_unit, n_hat, yaw_correction
    projected_vector = orientation_unit -  np.dot(orientation_unit, n_hat)*np.array(n_hat)
    x_correction = [5 - ekf_output.pose.pose.position.x, 0.0, 0.0]
    net_correction = projected_vector + x_correction
    orientation_unit = make_zero(orientation_unit)
    net_correction = make_zero(net_correction)
    cross_product = np.cross(orientation_unit, net_correction)
    correction_angle = angle_between(net_correction, orientation_unit)
    if(correction_angle == np.nan):
        correction_angle = 0
    yaw_correction = 1 
    if abs(5 - ekf_output.pose.pose.position.x) <= 0.05:
        if(x_correction[0] > 0):
            if x_correction[0]*orientation_unit[0] > 0:
                yaw_correction = 1
            else:
                yaw_correction = -1
        elif(x_correction[0] < 0):
            if x_correction[0]*orientation_unit[0] >= 0:
                yaw_correction = -1
            else:
                yaw_correction = 1
        yaw_correction = yaw_correction*abs(orientation_unit[0]) * (np.sign(orientation[1]))
    else:
        # if abs(x_correction[0]) <= 0.01:
        #     yaw_correction = yaw_correction*abs(correction_angle)*abs(x_correction[0]) * (np.sign(orientation[1])) * -1
        # else:
        #     yaw_correction = yaw_correction*abs(correction_angle)*abs(x_correction[0]) * (np.sign(orientation[1])) * (-np.sign(x_correction[0]))
        if cross_product[2] <= 0:
            yaw_correction = -yaw_correction*abs(correction_angle)*abs(x_correction[0])
        else:
            yaw_correction = yaw_correction*abs(correction_angle)*abs(x_correction[0])
    # print(correction_angle)
    if estimated_pose.pose.pose.position.z - 6.5 <= 0:
        yaw_correction = -yaw_correction
    print(yaw_correction)


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
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
    for i in range(len(vector)):
        if abs(vector[i]) <= 0.05:
            vector[i] = 0
    return vector



