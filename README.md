# Autonomous-Inspection-POC
Repository for the Development of an Autonomous wall-climbing Aircraft-Surface Inspection Robot

### Requirements
Ubuntu 20.04 LTS <br />
ROS2 - Foxy Distribution <br />
Gazebo 11.x <br />

### Installation Instructions
Step by step instructions to install Ubuntu, ROS2 and Gazebo are provided in the [Installation_Guide](docs/Installation_Guide.md)

### Launching the Simulation
1. Create a ROS workspace on your local PC as shown below
2. Clone the Autonomous-Inspection-POC repository to the /src directory of your ROS workspace
3. Open .bashrc file (type *gedit ~/.bashrc* in a terminal), add the following lines at the bottom and save the file.
4. Open a terminal, cd to your ROS workspace and build it (type *colcon build*)
5. Open a new terminal, cd to your ROS workspace and source it (type *. install local_setup.bash*)
6. Execute the iBot.launch.py launch file to launch gazebo and spawn the robot: (*ros2 launch gazebo iBot.launch.py*)
7. Repeat step 5. and execute the ibot_control.Launch.py launch file to make the robot move (*ros2 launch ibot_control ibot_control.launch.py*)

### Prerequisities to get you started ###
If you are completely new to ROS, I highly recommend you to go through the below tutorials in order, step by step. When you are done, you will have deep understanding of the ROS2 Navigaton Stack and will be ready to implement these in you own projects.

- [Testing ROS2 and Gazebo Integration](http://gazebosim.org/tutorials?tut=ros2_installing&cat=connect_ros)
- [ROS2 Tutorials](https://docs.ros.org/en/rolling/Tutorials.html)
- [ROS2 Basics in 5 Days](https://www.theconstructsim.com/wp-content/uploads/2019/03/ROS2-IN-5-DAYS-e-book.pdf)
- [Exploring ROS2 with wheeled robot - Youtube series](https://www.youtube.com/watch?v=T4iRJqESQAk&ab_channel=TheConstruct)
- [The Ultimate Guide to the ROS 2 Navigation Stack](https://automaticaddison.com/the-ultimate-guide-to-the-ros-2-navigation-stack/)
- [NAV2 Documentation - Setting up Odometry](https://navigation.ros.org/setup_guides/odom/setup_odom.html)
> **Note** Beginner level should suffice in the ealier stages and you can slowly build your skillset based on your requirements
