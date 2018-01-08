#!/usr/bin/env python

import cv2


class pattern_recognizer:

    def getRecognizedContours(self, image, patterns):
        grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        gaussed = cv2.GaussianBlur(grayImage, (5, 5), 0)

        cannyed = cv2.Canny(gaussed, 30, 150)

        (_, cnts, _) = cv2.findContours(cannyed.copy(),
                                        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        newCnts = []
        for cnt in cnts:
            for pattern in patterns:
                if cv2.matchShapes(pattern, cnt, cv2.CONTOURS_MATCH_I1, 0) < 0.01:
                    newCnts.append(cnt)

        contours = image.copy()
        cv2.drawContours(contours, newCnts, -1, (0, 255, 0), 2)

        # circles = cv2.HoughCircles(image.copy(), cv2.HOUGH_GRADIENT, 1, 20,param1=50,param2=30,minRadius=0,maxRadius=0)
        # for circle in circles[0,:]:
        #     cv2.circle(image, circle[0:1], circle[2], (0,255,0), 2)

        cv2.imshow("Contours", contours)

        cv2.waitKey(40)

        return newCnts
