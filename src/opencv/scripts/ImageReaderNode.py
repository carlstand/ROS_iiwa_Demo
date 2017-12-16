#!/usr/bin/env python

# Simple talker demo that published std_msgs/Strings messages
# to the 'chatter' topic

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


class ImageReader:
    def __init__(self):
        self.pub = rospy.Publisher('image_topic', Image, queue_size=10)
        rospy.init_node('ImageReader', anonymous=False)
        self.rate = rospy.Rate(25)
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)

    def run(self):
        while not rospy.is_shutdown():
            ret, frame = self.cap.read()
            cv2.imshow('frame', frame)
            cv2.waitKey(40)
            self.pub.publish(self.bridge.cv2_to_imgmsg(frame, "bgr8"))
            self.rate.sleep()


if __name__ == '__main__':
    try:
        ir = ImageReader()
        ir.run()
    except rospy.ROSInterruptException:
        # cv2.destroyAllWindows()
        pass
