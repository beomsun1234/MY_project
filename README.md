# MY_project

self driving car
use lidar, vesc , cam

RUN
1. run planner.launch ----> vesc_driver, lidar, map, amcl
2. run rosrun joy joy_node ->> joy_driver
3. run combin_control.py ---> move_base_pure_puresuit, parking , lane_detector 
