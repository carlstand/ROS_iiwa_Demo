#!/usr/bin/env python

import numpy as np
import cv2
import os
import sys

class Train():

    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        ret, self.img = self.cap.read()

        imgnew = self.img.copy()
        tmp = self.img.copy()

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.mouseCallBack)

        cv2.imshow('image', imgnew)

        self.cir = False
        self.rec = False
        self.ix = -1
        self.iy = -1
        self.jx = -1
        self.jy = -1
        self.ox = -1
        self.oy = -1

        path = sys.path[0] + '/train'
        isExists = os.path.exists(path)
        if isExists == False:
            os.mkdir(path)

        k = cv2.waitKey(0) & 0xFF
        if k == ord('s'):
            print 'write image'
            cv2.imwrite(path + '/train.jpg', self.img)
            self.draw(self.img, self.ix, self.iy, self.jx, self.jy, self.ox, self.oy)
            cv2.imwrite(path + '/pos.jpg', self.img)
            pos = np.array([self.ox, self.oy, min(self.ix, self.jx), min(self.iy, self.jy), max(self.ix, self.jx), max(self.iy, self.jy)])
            np.save(path + '/pos.npy', pos)

        cv2.destroyAllWindows()

    def draw(self, img, ix, iy, jx, jy, ox, oy):
        if (ix >= 0 and iy >= 0 and jx >= 0 and jy >= 0):
            cv2.rectangle(img, (ix, iy), (jx, jy), (0, 255, 0), 3)
        if (ox >= 0 and oy >= 0):
            cv2.circle(img, (ox, oy), 4, (0, 255, 0), 3)
        cv2.imshow('image', img)

    def mouseCallBack(self, event, x, y, flags, param):
        global ix, iy, jx, jy, ox, oy, drawing, cir, rec
        if event == cv2.EVENT_MBUTTONDOWN:
            cir = True
            imgnew = self.img.copy()
            self.ox = x
            self.oy = y

            self.draw(imgnew, self.ix, self.iy, self.jx, self.jy, self.ox, self.oy)

        elif event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            imgnew = self.img.copy()
            self.ix = x
            self.iy = y
            self.jx = -1
            self.jy = -1
        elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            if drawing == True:
                tmp = self.img.copy()
                self.draw(tmp, self.ix, self.iy, x, y, self.ox, self.oy)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            rec = True
            imgnew = self.img.copy()
            self.jx = x
            self.jy = y
            self.draw(imgnew, self.ix, self.iy, self.jx, self.jy, self.ox, self.oy)