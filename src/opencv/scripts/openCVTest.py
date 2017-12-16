#!/usr/bin/env python

import sys
import rospy
import cv2
import openCVLibs.patternReader as pr
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class image_converter:
    def __init__(self):
        # self.image_pub = rospy.Publisher("image_topic_2", Image, queue_size=10)

        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("image_topic", Image, self.callback)
        self.pr = pr.patternReader()

    def callback(self, data):

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        gaussed = cv2.GaussianBlur(image, (5, 5), 0)
        # cv2.imshow("Blurred", gaussed)

        cannyed = cv2.Canny(gaussed, 30, 150)
        # cv2.imshow("Canny", cannyed)

        (_, cnts, _) = cv2.findContours(cannyed.copy(),
                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        newCnts = []
        for cnt in cnts:
            for coin in self.pr.getPatternContour():
                if cv2.matchShapes(coin, cnt, 1, 0.0) < 0.001:
                    newCnts.append(cnt)

        print "I count %d coins in this image" % (len(newCnts))
        # print("got pics")
        contours = cv_image.copy()
        cv2.drawContours(contours, newCnts, -1, (0, 255, 0), 2)

        # circles = cv2.HoughCircles(image.copy(), cv2.HOUGH_GRADIENT, 1, 20,param1=50,param2=30,minRadius=0,maxRadius=0)
        # for circle in circles[0,:]:
        #     cv2.circle(image, circle[0:1], circle[2], (0,255,0), 2)

        cv2.imshow("Contours", contours)

        cv2.waitKey(40)

        # pass the image to the next node
        # try:
        #     self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
        # except CvBridgeError as e:
        #     print(e)


def main(args):
    image_converter()
    rospy.init_node('image_converter', anonymous=False)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)
