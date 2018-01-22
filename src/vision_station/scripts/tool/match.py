#!/usr/bin/env python

import cv2
import numpy as np
from matplotlib import pyplot as plt
import util
from geometry_msgs.msg import *
import time

class Match():

    def __init__(self):

        self.MIN_MATCH_COUNT = 2
        
        self.pos = np.load(sys.path[0] + '/train/pos.npy')
        self.invmtx = np.load(sys.path[0] + '/calib/invmtx.npy')

        self.cap = cv2.VideoCapture(0)

    def get_offset(self, job_name):

        img1 = cv2.imread(sys.path[0] + '/train/train.jpg')
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        
        ret, img2 = self.cap.read()
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        mask = np.zeros(img1.shape, np.uint8)
        roi = np.ones(((self.pos[5] - self.pos[3]), (self.pos[4] - self.pos[2])), np.uint8)
        mask[self.pos[3]:self.pos[5], self.pos[2]:self.pos[4]] = roi

        detector = cv2.xfeatures2d.SIFT_create()

        kp1, des1 = detector.detectAndCompute(img1, mask)
        kp2, des2 = detector.detectAndCompute(img2, None)

        grayout1 = cv2.drawKeypoints(img1, kp1, img1)
        grayout2 = cv2.drawKeypoints(img2, kp2, img2)

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
        search_params = dict(checks = 50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append(m)

        if len(good) > self.MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)
            matchesMask = mask.ravel().tolist()

            h, w = img1.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)

            img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

        else:
            print 'Not enough matches are found'
            matchesMask = None

        draw_params = dict(matchColor = (0,255,0),
            singlePointColor = None,
            matchesMask = matchesMask,
            flags = 2)

        img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

        ori_pt = self.pos[0:2].ravel().reshape(-1, 2)
        new_w_ori = util.image2board(self.invmtx, ori_pt)
        new_w_src = util.image2board(self.invmtx, src_pts)
        new_w_dst = util.image2board(self.invmtx, dst_pts)

        Mat = cv2.estimateRigidTransform(new_w_src, new_w_dst, False)

        r = util.getOffset2(Mat, new_w_ori)

        offset = Pose2D()
        offset.x = r[0]
        offset.y = r[1]
        offset.theta = r[2]

        time.sleep(2)
        return offset



'''

MIN_MATCH_COUNT = 2


pos = np.load('train/pos.npy')
invmtx = np.load('calib/invmtx.npy')

print 'invmtx'
print invmtx

img1 = cv2.imread('train/train.jpg')
img2 = cv2.imread('image/sample6.jpg')
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

detector = cv2.xfeatures2d.SIFT_create()
#detector = cv2.xfeatures2d.SURF_create()
#detector = cv2.ORB_create()

kp1, des1 = detector.detectAndCompute(img1, None)
kp2, des2 = detector.detectAndCompute(img2, None)

grayout1 = cv2.drawKeypoints(img1, kp1, img1)
cv2.imshow('out1', grayout1)
cv2.waitKey(0)

grayout2 = cv2.drawKeypoints(img2, kp2, img2)
cv2.imshow('out2', grayout2)
cv2.waitKey(0)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

if len(good) > MIN_MATCH_COUNT:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1.0)
    matchesMask = mask.ravel().tolist()

    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)

    img2 = cv2.polylines(img2, [np.int32(dst)], True, 255, 3, cv2.LINE_AA)

else:
    print 'Not enough matches are found'
    matchesMask = None

draw_params = dict(matchColor = (0,255,0),
    singlePointColor = None,
    matchesMask = matchesMask,
    flags = 2)

img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)

plt.imshow(img3), plt.show()

print 'src_pts'
print type(src_pts)
print src_pts
print 'dst_pts'
print type(dst_pts)
print dst_pts
print 'pos'
print type(pos)
print pos

ori_pt = pos[0:2].ravel().reshape(-1, 2)
new_w_ori = util.image2board(invmtx, ori_pt)
new_w_src = util.image2board(invmtx, src_pts)
new_w_dst = util.image2board(invmtx, dst_pts)

print 'new_w_ori'
print new_w_ori

Mat = cv2.estimateRigidTransform(new_w_src, new_w_dst, False)
print 'Mat'
print Mat

r = util.getOffset2(Mat, new_w_ori)
print 'r'
print r

'''
