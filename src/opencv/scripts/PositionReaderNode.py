#!/usr/bin/env python

import rospy
import cv2
from geometry_msgs.msg import PoseStamped


class PositionReader:

    def __init__(self):
        self.image_sub = rospy.Subscriber(
            "/visp_auto_tracker/object_position", PoseStamped, self.callback)
        self.pub = rospy.Publisher('object_position', PoseStamped, queue_size=10)
        rospy.init_node('PositionReader', anonymous=False)
        self.data = PoseStamped()

    def callback(self, data):
        if(self.data.pose.position.x != data.pose.position.x):
            self.pub.publish(data)
            print(data)
            self.data = data

if __name__ == '__main__':
    try:
        PositionReader()
        rospy.spin()
    except rospy.ROSInterruptException:
        cv2.destroyAllWindows()
        pass
