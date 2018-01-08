#!/usr/bin/env python

import rospy
import cv2
import camera_info_manager as cim
from sensor_msgs.msg import CameraInfo
from sensor_msgs.msg import Image


class CameraDriver:

    def __init__(self):
        self.ci = cim.CameraInfoManager(cname='my_camera', namespace='camera')
        self.image_sub = rospy.Subscriber("image_topic", Image, self.callback)
        rospy.init_node('CameraDriver', anonymous=False)

        self.pubInfo = rospy.Publisher('/camera/camera_info', CameraInfo, queue_size=10)
        self.pubImg = rospy.Publisher('/camera/image_raw', Image, queue_size=10)

    def callback(self, data):
        # print("image received")
        self.ci.loadCameraInfo()
        # print(self.ci.getCameraInfo())
        if(self.ci.isCalibrated()):
            cameraInfo = self.ci.getCameraInfo()
            # print(cameraInfo)
            self.pubInfo.publish(cameraInfo)
        
        self.pubImg.publish(data)


if __name__ == '__main__':
    try:
        CameraDriver()
        rospy.spin()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
