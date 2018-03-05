#!/usr/bin/env python

import sys
import copy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
# from moveit_commander import MoveGroupCommander

import rospy
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String


class iiwa_moveit:

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('iiwa_controller', anonymous=True)
        # self.rate = rospy.Rate(25)
        
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()

        self.group = moveit_commander.MoveGroupCommander("manipulator")
        # group.set_planning_time(1)
        self.group.set_planner_id("RRTConnectkConfigDefault")
        self.group.set_end_effector_link("iiwa_link_ee")
        
        self.image_sub = rospy.Subscriber(
            "/object_position", PoseStamped, self.callback)
        print("going to the start pose")
        self.current_pose = self.group.get_current_pose("iiwa_link_ee")
        self.group.set_start_state_to_current_state()
        print("start pose reached")

    def callback(self, data):
        # factor = 100
        pose_target = self.current_pose
        pose_target.pose.position.x = data.pose.position.x * 2
        pose_target.pose.position.y = data.pose.position.y * 2
        pose_target.pose.position.z = 0.89 + data.pose.position.z/2
        # pose_target.pose.orientation.w = data.pose.orientation.w
        # print(data.pose.position.z)
        # print(self.current_pose.pose.position.z)
        # print(pose_target.pose.position.x)
        print(self.group.get_current_pose("iiwa_link_ee").pose.position)

        # self.group.set_start_state_to_current_state()
        self.group.set_pose_target(pose_target, "iiwa_link_ee")

        self.group.plan()
        
        self.group.go(wait=True)


if __name__ == '__main__':
    try:
        iiwa_moveit()
        rospy.spin()
    except rospy.ROSInterruptException:
        moveit_commander.roscpp_shutdown()
        pass
