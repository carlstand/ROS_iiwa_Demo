#!/usr/bin/env python

import cv2


class patternReader:

    def __init__(self):
        self.image = cv2.imread(
            "/home/carlstand/ROS_iiwa_Demo/src/opencv/scripts/star.png")
        self.coin = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.coinGaussed = cv2.GaussianBlur(self.coin, (5, 5), 0)

        self.coinCannyed = cv2.Canny(self.coin, 150, 500)
        (_, self.coinCnts, _) = cv2.findContours(
            self.coinCannyed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print("patterns : {} ".format(len(self.coinCnts)))

    def getPatternContour(self):
        contours = self.image.copy()
        cv2.drawContours(contours, self.coinCnts, -1, (0, 255, 0), 2)
        cv2.imshow("pattern", contours)
        cv2.waitKey(40)
        return self.coinCnts


if __name__ == '__main__':
    pass
