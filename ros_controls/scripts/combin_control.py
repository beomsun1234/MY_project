#!/usr/bin/env python
#from _future_ import print_function
import os, rospkg
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
import parking as p
import move_base_pure_puresuit as m
import lane_detect_final as l
import lane_detector as c

class combind_control:
	def __init__(self):
		rospy.init_node('abc', anonymous=True)
		rospy.Subscriber("joy",Joy, self.joy_callback)
		rate = rospy.Rate(10)
		self.cruise_mode=0
		self.parking_mode=0
		self.lane_detection_mode = 0
		print("button x = cruise_mode , a = parking_mode, b = lane_detection_mode ")
		while not rospy.is_shutdown():
			if self.parking_mode ==1:
				print("START parking mode")
				p.simple_controller()
				print("exit")
			elif self.cruise_mode ==1:
				print("START cruise mode")
				m.pure_pursuit()
				print("GOAL Reached!")	
			elif self.lane_detection_mode == 1:
				print("START lane detect mode")
				c.run()
				print("END LANE")
			rate.sleep()
 
	def joy_callback(self, msg):
		self.cruise_mode = msg.buttons[0] ## button=x
		self.lane_detection_mode = msg.buttons[2] ## button=b 
		self.parking_mode = msg.buttons[1] ##button=a

if __name__ == '__main__':
	try:
		test = combind_control()
	except rospy.ROSInterruptException:
		pass

