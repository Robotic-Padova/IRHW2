#! /usr/bin/env python
from __future__ import print_function

import rospy
import actionlib

from tiago_iaslab_simulation import msg as ir_msg
from tiago_iaslab_simulation.srv import Objs
from utils import *


def send_pose(pos):
    client = actionlib.SimpleActionClient('/ir_pose', ir_msg.IRMoveAction)
    client.wait_for_server()

    goal = ir_msg.IRMoveGoal(position=pos)
    client.send_goal(goal)
    client.wait_for_result()
    return client.get_result()


def get_obj_ids():
    try:
        rospy.wait_for_service('human_objects_srv')
        get_ids = rospy.ServiceProxy('human_objects_srv', Objs)
        res = get_ids(1, 1)
        return res.ids

    except rospy.ServiceException as e:
        print("Service call failed: %s" % e)


def get_obj_pose(obj_id):
    client = actionlib.SimpleActionClient('/ir_detect', ir_msg.IRDetectAction)
    client.wait_for_server()

    def detect_feedback_callback(feedback):
        print("detect_feedback_callback", feedback)

    goal = ir_msg.IRDetectGoal(object_tag=obj_id)
    client.send_goal(goal, feedback_cb=detect_feedback_callback)
    client.wait_for_result()
    return client.get_result()


if __name__ == '__main__':
    try:
        rospy.init_node('ir_pose_client_test')
        result = send_pose([8, 0, 0])
        print("Result:", result.status)
        ids_ = get_obj_ids()
        print("ids:", result)

        # Robot stand up ....
        pass

        for id_ in ids_:
            # Do for each object

            # Check on the table:
            for angle in [1, 3, 4]:
                send_pose(pose_calc_table(angle=angle))
                obj_pos = get_obj_pose(id_)
                if len(obj_pos) != 0:
                    print('FINAL: ', obj_pos)
                    break
            # pick
            # send_pose(pose_calc_cyl(str(id_)))
            # put

    except rospy.ROSInterruptException:
        print("program interrupted before completion")