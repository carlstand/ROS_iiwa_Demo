# ROS_iiwa_Demo
set up a framework, and enable the iiwa to track a moving target

use case 1: camera mounted on the flange, the TCP will following a moving target, which carries a pre-defined feature, e.g. a toy train

## setup environments:
- sudo apt-get update
- sudo apt-get upgrade
- sudo apt-get install libvisp-dev visp-images-data ros-kinetic-visp ros-kinetic-vision-visp ros-kinetic-moveit ros-kinetic-camera-info-manager ros-kinetic-camera-info-manager-py ros-kinetic-camera-calibration python-catkin-tools
- pip3 install trollius [1]

## build wrokspace:
- cd {ROS_iiwa_Demo_folder}
- rosdep install --from-paths src --ignore-src -r -y
- catkin build
- source {ROS_iiwa_Demo_folder}/devel/setup.bash

[1]: maybe necessary for python3 builder