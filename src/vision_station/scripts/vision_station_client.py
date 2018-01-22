#!/usr/bin/env python

import rospy
from vision_station.srv import *

def add_two_ints_client():
    print "waiting for service : position_2d_service ..."
    rospy.wait_for_service('position_2d_service')
    print "service is ready."
    try:
        position_2d_service = rospy.ServiceProxy('position_2d_service', Position2DService)
        job_name = "job"
        resp1 = position_2d_service(job_name)
        print "[%f, %f, %f]"%(resp1.offset.x, resp1.offset.y, resp1.offset.theta)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    add_two_ints_client()