# ROS_iiwa_Demo
set up a framework, and enable the iiwa to track a moving target


## setup environments:
- sudo apt-get update
- sudo apt-get upgrade
- sudo apt-get install libvisp-dev visp-images-data ros-kinetic-visp ros-kinetic-vision-visp ros-kinetic-camera-info-manager-py ros-kinetic-camera-calibration


## steps:
- source /{ROS_iiwa_Demo_folder}/devel/setup.bash
- roslaunch opencv openCV.launch 
- rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.0138 image:=/image_topic camera:=/camera


A valid QR-code pattern that can be downloaded: https://github.com/lagadic/vision_visp/releases/download/vision_visp-0.5.0/template-qr-code.pdf
A Checkerborad example can be donloaded: http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration?action=AttachFile&do=get&target=check-108.pdf