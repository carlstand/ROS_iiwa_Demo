#!/usr/bin/env python

import cv2


class patternReader:

    def __init__(self):
        image = cv2.imread(
            "/home/carlstand/ROS_iiwa_Demo/src/opencv/scripts/coin.jpg")
        self.coin = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.coinGaussed = cv2.GaussianBlur(self.coin, (5, 5), 0)

        self.coinCannyed = cv2.Canny(self.coin, 150, 500)
        (_, self.coinCnts, _) = cv2.findContours(
            self.coinCannyed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        print("coins : {} ".format(len(self.coinCnts)))

    def getPatternContour(self):
        return self.coinCnts


if __name__ == '__main__':
    pass
