#!/usr/bin/env python

import numpy as np

def getAngle(sin, cos):
    result = np.arccos(cos)
    if (sin < 0):
        result = -result
    return result

def getOffset(mat, ori):
    x = mat[0][0]*ori[0]+mat[0][1]*ori[1]+mat[0][2]-ori[0]
    y = mat[1][0]*ori[0]+mat[1][1]*ori[1]+mat[1][2]-ori[1]
    a = getAngle(mat[1][0], mat[0][0])
    print mat[1][0]
    print mat[0][0]
    return (x, y, a)

def getOffset2(mat, ori):
    ori = ori.ravel().reshape(-1, 2)
    ori = np.column_stack((ori, np.ones((ori.shape[0], 1)))).T
    new_ori = np.dot(mat, ori)
    return (new_ori.ravel()[0] - ori.ravel()[0], new_ori.ravel()[1] - ori.ravel()[1], getAngle(mat[1][0], mat[0][0]))

def getNewPositions(mat, ori):
    r = ori.shape[0]
    result = np.zeros((r, 1, 2), np.float32)
    for k in range(0, r):
        result[k][0][0] = mat[0][0]*ori[k][0][1]+mat[0][1]*ori[k][0][0]+mat[0][2]
        result[k][0][1] = mat[1][0]*ori[k][0][1]+mat[1][1]*ori[k][0][0]+mat[1][2]
    return result

def homoMatrix(mat):
    h = mat.shape[0]
    w = mat.shape[1]
    for i in range(0, w):
        for j in range(0, h):
            mat[j][i] = mat[j][i]/mat[h-1][i]
    return mat

def image2board(invmtx, imgpts):
    imgpts = imgpts.ravel().reshape(-1, 2)
    imgpts = np.column_stack((imgpts, np.ones((imgpts.shape[0], 1)))).T
    brdpts = np.dot(invmtx, imgpts)
    brdpts = homoMatrix(brdpts)
    brdpts = brdpts[0:2,:].T.reshape(-1, 1, 2)
    return brdpts

if __name__ == "__main__":
    for angle in (0, 30, 90, 150, 180, 210, 270, 330):
        sin = np.sin(np.deg2rad(angle))
        cos = np.cos(np.deg2rad(angle))
        print np.rad2deg(getAngle(sin, cos))

    mat = np.array([[np.cos(np.deg2rad(45)), -np.sin(np.deg2rad(45)), 1],
        [np.sin(np.deg2rad(45)), np.cos(np.deg2rad(45)), 1-np.sqrt(2)]])
    ori = np.array([[[1.0, 1.0]]])
    print 'mat'
    print type(mat)
    print mat
    print 'ori'
    print type(ori)
    print ori
    x, y, a = getOffset2(mat, ori)
    print x
    print y
    print a
    