#!/usr/bin/env python

import numpy as np
import cv2
import glob
import os
import sys

class Calibrate():

    def __init__(self):

        # image size
        self.w = 9#input("w = ")
        self.h = 6#input("h = ")

        # square size [mm]
        self.size = 17.8#input("size[mm] = ")

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
        cv2.imshow('original image', gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (self.w, self.h), None)
        if ret == True:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), self.criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (self.w, self.h), corners2, ret)
            cv2.imshow('cornered image', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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

'''
def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (0,0,255), 3)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 3)
    #img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (255,0,0), 3)
    return img

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# square size [mm]
size = 1

# image size
w = 9
h = 6

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((h*w,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

img = cv2.imread('image/calibration.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Find the chess board corners
ret, corners = cv2.findChessboardCorners(gray, (w,h), None)

# If found, add object points, image points (after refining them)
if ret == True:
    objpoints.append(objp)

    corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    imgpoints.append(corners2)
 
    # Draw and display the corners
    img = cv2.drawChessboardCorners(img, (w,h), corners2, ret)
    cv2.imshow('img',img)
    cv2.waitKey(0)

cv2.destroyAllWindows()

print 'objpoints'
print objpoints
print 'imgpoints'
print imgpoints

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print 'ret'
print ret
print 'mtx'
print mtx
print 'dist'
print dist
print 'rvecs'
print rvecs
print 'tvecs'
print tvecs

rmtx = cv2.Rodrigues(rvecs[0])
print 'rmtx'
print type(rmtx)
print rmtx

print 'rmtx0'
print type(rmtx[0])
print rmtx[0]

exmtx = np.column_stack((rmtx[0], tvecs[0]))
print 'exmtx'
print type(exmtx)
print exmtx

matrix = np.dot(mtx, exmtx)
print 'matrix'
print type(matrix)
print matrix

homomtx = np.column_stack((matrix[:,0:2], matrix[:,3]))
print 'homomtx'
print type(homomtx)
print homomtx

invmtx = np.linalg.inv(homomtx)
print 'invmtx'
print type(invmtx)
print invmtx

axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
print 'axis'
print type(axis)
print axis

origin = np.array([[0.0], [0.0], [0.0], [1.0]])
xaxis = np.array([[3.0], [0.0], [0.0], [1.0]])
yaxis = np.array([[0.0], [3.0], [0.0], [1.0]])

imgpts = np.dot(matrix, origin)
oripts = imgpts/imgpts[2][0]
imgpts = np.dot(matrix, xaxis)
xpts = imgpts/imgpts[2][0]
imgpts = np.dot(matrix, yaxis)
ypts = imgpts/imgpts[2][0]

print 'oripts'
print type(oripts)
print oripts.astype(int)
print type(tuple(oripts.flatten()))
print tuple(oripts.flatten())

cv2.line(img, tuple(oripts.astype(int).flatten()[0:2]), tuple(xpts.astype(int).flatten()[0:2]), (0,0,255), 3)
cv2.line(img, tuple(oripts.astype(int).flatten()[0:2]), tuple(ypts.astype(int).flatten()[0:2]), (0,255,0), 3)
cv2.imshow('img',img)

isExists = os.path.exists('calib')
if isExists == False:
    os.mkdir('calib')

k = cv2.waitKey(0) & 0xFF
if k == ord('s'):
    print 'write image'
    cv2.imwrite('calib/calibrated.jpg', img)
cv2.destroyAllWindows()

np.save('calib/ret.npy', ret)
np.save('calib/mtx.npy', mtx)
np.save('calib/dist.npy', dist)
np.save('calib/rvecs.npy', rvecs)
np.save('calib/tvecs.npy', tvecs)
np.save('calib/size.npy', size)
np.save('calib/matrix.npy', matrix)
np.save('calib/invmtx.npy', invmtx)
'''




'''

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

isExists = os.path.exists('calib')
if isExists == False:
	os.mkdir('calib')

np.save('calib/ret.npy', ret)
np.save('calib/mtx.npy', mtx)
np.save('calib/dist.npy', dist)
np.save('calib/rvecs.npy', rvecs)
np.save('calib/tvecs.npy', tvecs)
np.save('calib/size.npy', size)

mtx = np.load('calib/mtx.npy')
dist = np.load('calib/dist.npy')
rvecs = np.load('calib/rvecs.npy')
tvecs = np.load('calib/tvecs.npy')


axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
print axis
# project 3D points to image plane
imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
print imgpts

img = draw(img,corners2,imgpts)
cv2.imshow('img',img)
k = cv2.waitKey(0) & 0xFF
if k == ord('s'):
	print 'write image'
	cv2.imwrite('calib/calibrated.jpg', img)

cv2.destroyAllWindows()


points = np.array([
    [[0.0, 0.0, 0.0]],
    [[1.0, 0.0, 0.0]],
    [[2.0, 0.0, 0.0]],
    [[0.0, 1.0, 0.0]],
    [[1.0, 1.0, 0.0]],
    [[2.0, 1.0, 0.0]],
    [[0.0, 2.0, 0.0]],
    [[1.0, 2.0, 0.0]],
    [[2.0, 2.0, 0.0]]])
print 'points'
print type(points)
print points

points2d = np.array([
    [[0.0, 0.0]],
    [[1.0, 0.0]],
    [[2.0, 0.0]],
    [[0.0, 1.0]],
    [[1.0, 1.0]],
    [[2.0, 1.0]],
    [[0.0, 2.0]],
    [[1.0, 2.0]],
    [[2.0, 2.0]]])
print 'points2d'
print type(points2d)
print points2d

imagepoints, imagejac = cv2.projectPoints(points, rvecs, tvecs, mtx, dist)
print 'imagepoints'
print type(imagepoints)
print imagepoints

Mat = cv2.estimateRigidTransform(points2d, imagepoints, False)
print 'Mat'
print Mat

M, mask = cv2.findHomography(points2d, imagepoints)
print 'M'
print M
'''