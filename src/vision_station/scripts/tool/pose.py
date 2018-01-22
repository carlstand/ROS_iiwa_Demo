import numpy as np
import cv2
import glob

mtx = np.load('calib/mtx.npy')
dist = np.load('calib/dist.npy')
rvecs = np.load('calib/rvecs.npy')
tvecs = np.load('calib/tvecs.npy')

# image size
w = 9
h = 6

print mtx
print dist

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0))
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0))
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255))
    return img

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((h*w,3), np.float32)
objp[:,:2] = np.mgrid[0:w,0:h].T.reshape(-1,2)

#axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]])
print 'axis : '
print type(axis)
print axis

axis = axis.reshape(-1, 3)
print 'axis : '
print type(axis)
print axis

start = np.float32([[0, 0, 0]])
end = np.float32([[3, 0, 0]])
print 'axis : '
print type(axis)
print axis

for fname in glob.glob('image/calibration.jpg'):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # project 3D points to image plane
    startpts, jac = cv2.projectPoints(start, rvecs, tvecs, mtx, dist)
    endpts, jac = cv2.projectPoints(end, rvecs, tvecs, mtx, dist)

    print 'startpts'
    print type(startpts)
    print startpts
    print 'endpts'
    print type(endpts)
    print endpts

    startpts = tuple(startpts.ravel())
    endpts = tuple(endpts.ravel())
    print 'startpts'
    print type(startpts)
    print startpts
    print 'endpts'
    print type(endpts)
    print endpts

    img = cv2.line(img, startpts, endpts, (255,0,0))
    cv2.imshow('img', img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
