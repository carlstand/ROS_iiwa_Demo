#!/usr/bin/env python

import rospy
import cv2
import openCVLibs.patternReader as pr
import openCVLibs.patternRecognize as prer
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class ImageToPositionNode:

    def __init__(self):

        self.image_sub = rospy.Subscriber("image_topic", Image, self.callback)
        rospy.init_node('ImageTo2DPosition', anonymous=False)

        self.bridge = CvBridge()
        self.pr = pr.patternReader()
        self.prer = prer.pattern_recognizer()

    def callback(self, data):

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        contours = self.prer.getRecognizedContours(cv_image, self.pr.getPatternContour())

        print("found {} contours.".format(len(contours)))


if __name__ == '__main__':
    try:
        ImageToPositionNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
