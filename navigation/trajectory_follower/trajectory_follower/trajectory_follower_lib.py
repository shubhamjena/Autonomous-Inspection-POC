from .trajectory_follower_includes import *

def node_init(self):

    # SUBSCRIBERS

    # PUBLISHERS

    self.thrust_publisher = self.create_publisher(Wrench, '/iBot/gazebo_ros_force', 10)
    self.velocity_publisher = self.create_publisher(Twist, '/iBot/cmd_vel', 10)

    # SERVICES

    # PUBLISHER TIMERS

    timer_period = 0.1  # seconds
    self.thrust_timer = self.create_timer(timer_period, self.thrust_timer_callback)
    self.velocity_timer = self.create_timer(timer_period, self.velocity_timer_callback)
    
    # EXTRA TIMERS
    

#* CALLBACKS

#* SUBSCRIBER CALLBACKS

#* PUBLISHER CALLBACKS

def thrust_timer_callback(self):
    wrench = Wrench()
    wrench.force.z = -1000.0
    self.thrust_publisher.publish(wrench)

def velocity_timer_callback(self):
    twist = Twist()
    twist.linear.x = -0.1
    self.velocity_publisher.publish(twist)

