# Title:

The Repository contains prj_finalerobo package, which includes final.py and the launch file with start.launch.


# Getting started:

1. It is required to know the current position of robot, which is subscribed from /amcl_pose topic to localize the turtlebot in the given map. 
2. To access the destination points, It is required to subscribe to /goals topic.
3. Creating an action client that communicates with action server /move_base that uses a message MoveBaseAction.

# General description:

The goal of this project is to reach as many goals as possible, avoiding the obstacles in between and also collision with other robots.

# Algorithm description:


1. To start with, all the goal points are appended in one list called list1.
2. In the second list named sort_list, appended the current position of the robot.
3. Calculated the euclidean distance for every goal point from list1 with the current position from sort_list.
4. The point which has minimum distance is than appended in the sort_list.
5. The robot moves to the desination goal point.
6. The same procedure is repeated for all the goal points.

The below Figure is the pictorial representation of the algorithm.

![](https://github.com/Sai99897/goal-sort-and-nav-with-tiago/blob/main/process.png)

# References:
 
 1. https://www.youtube.com/watch?v=mYwIu4OVMR8
 2. http://wiki.ros.org/move_base
 3. http://wiki.ros.org/navigation/Tutorials/SendingSimpleGoals# Goal-sorting-and-navigation-with-Turtlebot
# Goal-sorting-and-navigation-with-Turtlebot
# navigation_with_tiago
