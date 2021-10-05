# Autonomous-Inspection-POC
Repository for the Development of an Autonomous Aircraft - Surface Inspection Robot

### Requirements
Ubuntu 20.04 LTS <br />
ROS2 - Foxy Distribution <br />
Gazebo 11.x <br /> 

### Installation of Ubuntu 20.04
The detalied instructions on how to install Ubuntu 20.04 are documented [here](https://phoenixnap.com/kb/install-ubuntu-20-04). <br />

> **Note** The entire installation process might take some time. This includes the download of installation media (.iso) file which is approximately ~2.9 Gb, creating a bootable USB and installing the OS.

### Installation of ROS 2 Foxy on Ubuntu
The official steps for installing ROS are at [this link at ROS.org](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html), but I will walk you through the process below so that you can see what each step should look like. We will install ROS 2 Foxy via Debian Packages. </br>

#### Set the Locale ####
The first thing we are going to do is to set the locale. You can understand what locale means [at this link](https://en.wikipedia.org/wiki/Locale_(computer_software)). <br />
Type this command inside terminal window <br />
```
locale
```
![image](https://user-images.githubusercontent.com/17789814/135904022-75d444a3-8905-4087-9bdf-d1dc30571e1c.png)

Now type the following command
```
sudo apt update && sudo apt install locales
```    
Wait for everything to install, and then type:
```
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```    
Now type locale and verify whether terminal is same as shown in the above image
    
#### Add the ROS 2 Repositories ####
Type the following inside the terminal. 
``` 
sudo apt update && sudo apt install curl gnupg2 lsb-release
``` 
At the prompt, type Y and then Enter to install the repositories.<br />

Now type the following command (this is a single command. you can copy and paste all this into your terminal window):

``` 
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
``` 
Now let’s add the repository to the source list.

``` 
sudo sh -c 'echo "deb [arch=$(dpkg --print-architecture)] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list
``` 
#### Install the ROS 2 Packages ####
Update the apt repository cache.

``` 
sudo apt update

``` 
Install the Desktop version of ROS 2.

``` 
sudo apt install ros-foxy-desktop

``` 
Type Y and Enter to download ROS 2.

#### Set up the Environment Variables ####
Add foxy to your bash file.

```
echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc
```
To check if it was added, type the following command, and scroll all the way to the bottom.:
```
gedit ~/.bashrc
```
![image](https://user-images.githubusercontent.com/17789814/136082203-443d738e-9f9d-4710-b7ac-c31457ebfe6f.png)

If not, type the command and manually edit ~/.bashrc file by copy pasting the source command
``` 
gedit ~/.bashrc 
``` 
Now close the current terminal window, and open a new one.

Type the following command to see what version of ROS you are using.
``` 
printenv ROS_DISTRO
``` 
Here is what you should see. <br />
![image](https://user-images.githubusercontent.com/17789814/136082855-8dd07c37-9b82-416e-83e3-f7189bb426fd.png)

You can also type:
```
env |grep ROS
```
