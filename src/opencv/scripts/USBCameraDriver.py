#!/usr/bin/env python

import rospy
import cv2
import camera_info_manager as cim
from sensor_msgs .msg import CameraInfo
from sensor_msgs.msg import Image


class CameraDriver:

    def __init__(self):
        self.ci = cim.CameraInfoManager(cname='my_camera',namespace='camera')
        self.image_sub = rospy.Subscriber("image_topic", Image, self.callback)
        rospy.init_node('CameraDriver', anonymous=False)

    def callback(self, data):
        # print("image received")
        self.ci.loadCameraInfo()
        # print(self.ci.getCameraInfo())
        if(self.ci.isCalibrated()):
            print(self.ci.getCameraInfo())


if __name__ == '__main__':
    try:
        CameraDriver()
        rospy.spin()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
