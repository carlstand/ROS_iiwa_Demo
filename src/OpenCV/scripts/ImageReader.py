#!/usr/bin/env python

# Simple talker demo that published std_msgs/Strings messages
# to the 'chatter' topic

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
# from std_msgs.msg import String


def ImageReader():
    pub = rospy.Publisher('image_topic', Image, queue_size=10)
    rospy.init_node('ImageReader', anonymous=True)
    rate = rospy.Rate(0.5)
    img = cv2.imread("example.png")
    bridge = CvBridge()
    while not rospy.is_shutdown():
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        pub.publish(bridge.cv2_to_imgmsg(img, "bgr8"))
        rate.sleep()


if __name__ == '__main__':
    try:
        ImageReader()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
