import numpy as np
import cv2
import math
import rospy
from std_msgs.msg import Float64,String
import random

import matplotlib.pyplot as plt

from nav_msgs.msg import Path,Odometry
from geometry_msgs.msg import PoseStamped
class purePursuit:
	def __init__(self, lfd):
		self.is_look_forward_point=False
		self.vehicle_length=0.5

		self.lfd=lfd
		self.min_lfd=0.7
		self.max_lfd=1.2

		self.lpath_sub = rospy.Subscriber('/lane_path',Path, self.lane_path_callback)


		self.speed_pub = rospy.Publisher('/commands/motor/speed', Float64, queue_size=1)

		self.position_pub = rospy.Publisher('/commands/servo/position', Float64, queue_size=1)
		self.lpath = None
	
	def lane_path_callback(self, msg):
		self.lpath = msg

	def steering_angle(self):

		self.is_look_forward_point = False

		for i in self.lpath.poses:

			path_point=i.pose.position

			if path_point.x>0:
				dis_i = np.sqrt(np.square(path_point.x)+np.square(path_point.y))

				if dis_i >= self.lfd:
					self.is_look_forward_point = True
					break
		theta= math.atan2(path_point.y, path_point.x)

		if self.is_look_forward_point:
			steering_deg=math.atan2((2*self.vehicle_length*math.sin(theta)), self.lfd)*180/math.pi

			self.steering=np.clip(steering_deg, -17,17)/34+0.5
			print(self.steering)
		else:
			self.steering=0.5
			print("no found forward point")
	
	def pub_cmd(self, control_speed, steer_lv):
		#self.position_pub.publish(self.steering)
		#Servo Steer Level: 0.15(L) - 0.5304(C) - 0.85(R)
		if steer_lv < 0.15: steer_lv = 0.15
		if steer_lv > 0.85: steer_lv = 0.85
		
		self.position_pub.publish(steer_lv)
		self.speed_pub.publish(control_speed)

