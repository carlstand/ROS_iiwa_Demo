#!/usr/bin/env python

import rospy
import cv2
import camera_info_manager_py as cim
from sensor_msgs .msg import CameraInfo
from sensor_msgs.msg import Image


class CameraDriver:

    def __init__(self):
        self.ci = cim.CameraInfoManager(cname='mono_camera')
        self.image_sub = rospy.Subscriber("image_topic", Image, self.callback)
        rospy.init_node('ImageTo2DPosition', anonymous=False)

    def callback(self, data):
        self.ci.loadCameraInfo()
        if(self.ci.ifisCalibrated()):
            print(self.ci.getCameraInfo())


if __name__ == '__main__':
    try:
        CameraDriver()
        rospy.spin()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
