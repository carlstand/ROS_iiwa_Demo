#!/usr/bin/env python

import rospy
import cv2
from geometry_msgs.msg import PoseStamped


class PositionReader:

    def __init__(self):
        self.image_sub = rospy.Subscriber("/visp_auto_tracker/object_position", PoseStamped, self.callback)
        rospy.init_node('PositionReader', anonymous=False)
        self.data = None

    def callback(self, data):
        print(data)


if __name__ == '__main__':
    try:
        PositionReader()
        rospy.spin()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
