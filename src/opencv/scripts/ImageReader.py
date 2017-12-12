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
    rospy.init_node('ImageReader', anonymous=False)
    rate = rospy.Rate(25)
    bridge = CvBridge()
    cap = cv2.VideoCapture(0)
    while not rospy.is_shutdown():
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the resulting frame
        cv2.imshow('frame', gray)
        cv2.waitKey(40)
        # hello_str = "hello world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        pub.publish(bridge.cv2_to_imgmsg(gray, "mono8"))
        rate.sleep()


if __name__ == '__main__':
    try:
        ImageReader()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
