#!/usr/bin/env python
import rospy
import math
from goal_publisher.msg import PointArray
from geometry_msgs.msg import PoseWithCovarianceStamped
from tf import transformations
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Twist
import actionlib
from move_base_msgs.msg import MoveBaseGoal, MoveBaseAction, MoveBaseResult

# Defining a list - goals_list
goals_list = list()

# Callback function for the /goals topic Subscriber
def callback_goalpoint(msg):
    global goals_list
    for i in range(len(msg.goals)):
        goals_list.append([msg.goals[i].x, msg.goals[i].y])

def callback_position(pos):
    global current_x_pos
    global current_y_pos
    global current_theta
    current_x_pos = pos.pose.pose.position.x
    current_y_pos = pos.pose.pose.position.y
    rot_q=pos.pose.pose.orientation
    (roll,pitch,current_theta)=euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z,rot_q.w])


# Crearting the goal message and sending it to the action server
def goal_struct(point):
    my_goals = MoveBaseGoal()
    my_goals.target_pose.header.frame_id = "map"
    my_goals.target_pose.pose.position.x = point[0]
    my_goals.target_pose.pose.position.y = point[1]
    my_goals.target_pose.pose.position.z = 0
    my_goals.target_pose.pose.orientation.x = 0
    my_goals.target_pose.pose.orientation.y = 0
    my_goals.target_pose.pose.orientation.z = 0
    my_goals.target_pose.pose.orientation.w = 1
    return my_goals

# Initialize node
rospy.init_node("prj_finale")
#id=rospy.get_namespace()

# Subscribe to /goals topic to fetch the goal points
sub = rospy.Subscriber("/goals", PointArray, callback_goalpoint, queue_size=1)

# Subscribe to /amcl_pose topic to localize the turtlebot in the given map
sub_loc = rospy.Subscriber("amcl_pose", PoseWithCovarianceStamped , callback_position)

# Creating an action client that communicates with action server /move_base that uses a message MoveBaseAction
client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
# Action client waits for the action server to be launched and then sends the goals to the server

client.wait_for_server()
rate = rospy.Rate(2)

#waiting for goals to subscribe
while not goals_list:
    rospy.sleep(0.1)
list1 = goals_list


sort_list = [[current_x_pos,current_y_pos]]
while (len(list1) > 0):
    x1 = sort_list[-1][0]
    y1 = sort_list[-1][1]
    list2 = []
    for i in range(len(list1)):
        d = math.sqrt((list1[i][0]-x1)**2 + (list1[i][1]-y1)**2)
        list2.append(d)
    sort_list.append(list1[list2.index(min(list2))])
    list1.remove(list1[list2.index(min(list2))])
sort_list.remove([current_x_pos,current_y_pos])
print(sort_list)

while not rospy.is_shutdown():

    for i in range(len(sort_list)):
        goal= goal_struct(sort_list[i])
        rospy.sleep(2)
        client.send_goal(goal)
        client.wait_for_result(rospy.Duration(60))
        x=goal.target_pose.pose.position.x
        y=goal.target_pose.pose.position.y
        d=math.sqrt((current_x_pos-x)**2 + (current_y_pos-y)**2)

        if client.get_state() == 3 or d<0.015:
            print("Goal {} has reached!".format(i))
            rospy.sleep(1)
        else:
            client.cancel_goal()
