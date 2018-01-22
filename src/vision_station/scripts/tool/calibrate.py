#!/usr/bin/env python

import numpy as np
import cv2
import glob
import os
import sys

class Calibrate():

    def __init__(self):

        # image size
        self.w = input("w = ")
        self.h = input("h = ")

        # square size [mm]
        self.size = input("size[mm] = ")

        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((self.h * self.w, 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.w, 0:self.h].T.reshape(-1, 2)
        objp = objp * self.size

        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.

        self.cap = cv2.VideoCapture(0)
        ret, img = self.cap.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (self.w, self.h), None)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (self.w, self.h), corners2, ret)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        rmtx = cv2.Rodrigues(rvecs[0])
        exmtx = np.column_stack((rmtx[0], tvecs[0]))
        matrix = np.dot(mtx, exmtx)
        homomtx = np.column_stack((matrix[:,0:2], matrix[:,3]))
        invmtx = np.linalg.inv(homomtx)

        origin = np.array([[0.0], [0.0], [0.0], [1.0]])
        xaxis = np.array([[3.0 * self.size], [0.0], [0.0], [1.0]])
        yaxis = np.array([[0.0], [3.0 * self.size], [0.0], [1.0]])

        imgpts = np.dot(matrix, origin)
        oripts = imgpts / imgpts[2][0]
        imgpts = np.dot(matrix, xaxis)
        xpts = imgpts / imgpts[2][0]
        imgpts = np.dot(matrix, yaxis)
        ypts = imgpts / imgpts[2][0]

        cv2.line(img, tuple(oripts.astype(int).flatten()[0:2]), tuple(xpts.astype(int).flatten()[0:2]), (0,0,255), 3)
        cv2.line(img, tuple(oripts.astype(int).flatten()[0:2]), tuple(ypts.astype(int).flatten()[0:2]), (0,255,0), 3)
        cv2.imshow('calibrated image', img)

        path = sys.path[0] + '/calib'
        isExists = os.path.exists(path)
        if isExists == False:
            print 'make dir'
            os.mkdir(path)

        k = cv2.waitKey(0) & 0xFF
        if k == ord('s'):
            print 'write image'
            cv2.imwrite(path + '/calibrated.jpg', img)
            np.save(path + '/invmtx.npy', invmtx)
        cv2.destroyAllWindows()