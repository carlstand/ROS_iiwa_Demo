#!/usr/bin/env python

from vision_station.srv import *
from geometry_msgs.msg import *
from tool.calibrate import *
from tool.train import *
from tool.match import *
import rospy
import sys

class Vision_Station_Server():

    def __init__(self, process):
        flag = int(process)
        if (flag % 2 == 1):
            print "run step 1"
            Calibrate()

        flag = flag / 2
        if (flag % 2 == 1):
            print "run step 2"
            Train()

        flag = flag / 2
        if (flag % 2 == 1):
            print "run step 3"
            rospy.init_node('vision_station_server')
            s = rospy.Service('position_2d_service', Position2DService, self.handle_position_2d_service)
            print "Ready to accept request"
            rospy.spin()

    def handle_position_2d_service(self, req):
        print "Receive request : %s"%(req.job_name)
        match = Match()
        offset = match.get_offset(req.job_name)
        print "Result received."
        return Position2DServiceResponse(offset)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process = sys.argv[1]
    else:
        process = 4

    Vision_Station_Server(process)