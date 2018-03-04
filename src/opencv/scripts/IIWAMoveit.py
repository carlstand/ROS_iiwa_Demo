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

    def move_group_python_interface_tutorial(self):
        # BEGIN_TUTORIAL
        #
        # Setup
        # ^^^^^
        # CALL_SUB_TUTORIAL imports
        #
        # First initialize moveit_commander and rospy.
        print "============ Starting tutorial setup"
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('move_group_python_interface_tutorial',
                        anonymous=True)

        # Instantiate a RobotCommander object.  This object is an interface to
        # the robot as a whole.
        robot = moveit_commander.RobotCommander()

        # Instantiate a PlanningSceneInterface object.  This object is an interface
        # to the world surrounding the robot.
        scene = moveit_commander.PlanningSceneInterface()

        # Instantiate a MoveGroupCommander object.  This object is an interface
        # to one group of joints.  In this case the group is the joints in the left
        # arm.  This interface can be used to plan and execute motions on the left
        # arm.
        group = moveit_commander.MoveGroupCommander("manipulator")
        # group.set_planning_time(1)
        group.set_planner_id("RRTConnectkConfigDefault")
        group.set_end_effector_link("iiwa_link_ee")
        rate = rospy.Rate(25)
        print "============ Generating plan 1"
        d = 1
        while not rospy.is_shutdown():
            d = d * -1
            pose_target = group.get_current_pose()

            pose_target.pose.position.z -= d * 0.10
            group.set_pose_target(pose_target)

            # Now, we call the planner to compute the plan
            # and visualize it if successful
            # Note that we are just planning, not asking move_group
            # to actually move the robot
            plan1 = group.plan()

            # print "============ Waiting while RVIZ displays plan1..."
            # rospy.sleep(5)

            # You can ask RVIZ to visualize a plan (aka trajectory) for you.  But the
            # group.plan() method does this automatically so this is not that useful
            # here (it just displays the same trajectory again).
            # print "============ Visualizing plan1"
            # display_trajectory = moveit_msgs.msg.DisplayTrajectory()

            # display_trajectory.trajectory_start = robot.get_current_state()
            # display_trajectory.trajectory.append(plan1)
            # display_trajectory_publisher.publish(display_trajectory)

            # print "============ Waiting while plan1 is visualized (again)..."
            # rospy.sleep(5)

            # Moving to a pose goal
            # ^^^^^^^^^^^^^^^^^^^^^
            #
            # Moving to a pose goal is similar to the step above
            # except we now use the go() function. Note that
            # the pose goal we had set earlier is still active
            # and so the robot will try to move to that goal. We will
            # not use that function in this tutorial since it is
            # a blocking function and requires a controller to be active
            # and report success on execution of a trajectory.

            # Uncomment below line when working with a real robot
            group.execute(plan1, wait=True)
            rate.sleep()
        # Planning to a joint-space goal
        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        #
        # Let's set a joint space goal and move towards it.
        # First, we will clear the pose target we had just set.

        group.clear_pose_targets()

        # # Then, we will get the current set of joint values for the group
        # group_variable_values = group.get_current_joint_values()
        # print "============ Joint values: ", group_variable_values

        # # Now, let's modify one of the joints, plan to the new joint
        # # space goal and visualize the plan
        # group_variable_values[0] = 1.0
        # group.set_joint_value_target(group_variable_values)

        # plan2 = group.plan()

        # print "============ Waiting while RVIZ displays plan2..."
        # rospy.sleep(5)

        # # Cartesian Paths
        # # ^^^^^^^^^^^^^^^
        # # You can plan a cartesian path directly by specifying a list of waypoints
        # # for the end-effector to go through.
        # waypoints = []

        # # start with the current pose
        # waypoints.append(group.get_current_pose().pose)

        # # first orient gripper and move forward (+x)
        # wpose = geometry_msgs.msg.Pose()
        # wpose.orientation.w = 1.0
        # wpose.position.x = waypoints[0].position.x + 0.1
        # wpose.position.y = waypoints[0].position.y
        # wpose.position.z = waypoints[0].position.z
        # waypoints.append(copy.deepcopy(wpose))

        # # second move down
        # wpose.position.z -= 0.10
        # waypoints.append(copy.deepcopy(wpose))

        # # third move to the side
        # wpose.position.y += 0.05
        # waypoints.append(copy.deepcopy(wpose))

        # # We want the cartesian path to be interpolated at a resolution of 1 cm
        # # which is why we will specify 0.01 as the eef_step in cartesian
        # # translation.  We will specify the jump threshold as 0.0, effectively
        # # disabling it.
        # (plan3, fraction) = group.compute_cartesian_path(
        #     waypoints,   # waypoints to follow
        #     0.01,        # eef_step
        #     0.0)         # jump_threshold

        # print "============ Waiting while RVIZ displays plan3..."
        # rospy.sleep(5)

        # # Adding/Removing Objects and Attaching/Detaching Objects
        # # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # # First, we will define the collision object message
        # collision_object = moveit_msgs.msg.CollisionObject()

        # When finished shut down moveit_commander.
        moveit_commander.roscpp_shutdown()

        # END_TUTORIAL

        print "============ STOPPING"


if __name__ == '__main__':
    try:
        mi = iiwa_moveit()
        mi.move_group_python_interface_tutorial()
    except rospy.ROSInterruptException:
        pass
