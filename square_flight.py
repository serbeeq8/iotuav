#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode, CommandBool
import time

# Callback function to update the current state
current_state = None

def state_cb(msg):
    global current_state
    current_state = msg

def wait_for_connection():
    global current_state
    while not rospy.is_shutdown() and current_state is None:
        rospy.loginfo("Waiting for state message...")
        rate.sleep()

    while not rospy.is_shutdown() and not current_state.connected:
        rospy.loginfo("Waiting for connection...")
        rate.sleep()

def arm_drone():
    rospy.wait_for_service('/mavros/cmd/arming')
    try:
        arm_service = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
        arm_service(True)
        rospy.loginfo("Arming command sent!")
    except rospy.ServiceException as e:
        rospy.logerr("Failed to arm: %s" % e)

def set_guided_mode():
    rospy.wait_for_service('/mavros/set_mode')
    try:
        set_mode_service = rospy.ServiceProxy('/mavros/set_mode', SetMode)
        set_mode_service(base_mode=0, custom_mode="GUIDED")
        rospy.loginfo("GUIDED mode set!")
    except rospy.ServiceException as e:
        rospy.logerr("Failed to set GUIDED mode: %s" % e)

def move_to_position(x, y, z, pose_pub):
    pose = PoseStamped()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = z
    pose_pub.publish(pose)
    time.sleep(5)

if __name__ == "__main__":
    rospy.init_node("guided_square")

    state_sub = rospy.Subscriber("/mavros/state", State, state_cb)
    pose_pub = rospy.Publisher("/mavros/setpoint_position/local", PoseStamped, queue_size=10)

    rate = rospy.Rate(20)  # 20Hz

    wait_for_connection()

    # Initializing position
    initial_pose = PoseStamped()
    initial_pose.pose.position.x = 0
    initial_pose.pose.position.y = 0
    initial_pose.pose.position.z = 15

    for _ in range(100):
        pose_pub.publish(initial_pose)
        rate.sleep()

    arm_drone()
    set_guided_mode()

    # Define the square path where we fix the altitude as 15 meters
    waypoints = [
        (0, 0, 15),
        (10, 0, 15),
        (10, 10, 15),
        # (0, 10, 15),
        (0, 0, 15)
    ]

    # Move through the waypoints
    for point in waypoints:
        move_to_position(point[0], point[1], point[2], pose_pub)
        rospy.loginfo(f"Moving to position: {point}")

    rospy.loginfo("Completed square pattern.")

    rospy.spin()

