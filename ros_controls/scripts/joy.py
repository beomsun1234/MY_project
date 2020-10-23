#!/usr/bin/env python
#from _future_ import print_function

import rospy
import rospkg
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped 
from math import pi, cos, sin , sqrt, pow , atan2


class pure_pursuit:
    def __init__(self):
        rospy.init_node('make_path', anonymous=True)
        rospy.Subscriber("joy",Joy, self.joy_callback)
	self.speed=0
	self.steel = 0
        self.motor_pub = rospy.Publisher('commands/motor/speed', Float64, queue_size=1)
	self.servo_pub = rospy.Publisher('commands/servo/position', Float64, queue_size=1)

    
        self.motor_msg = Float64()
	self.servo_msg=Float64()

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
    		self.motor_msg.data=self.speed*2000
		if -0.5 <self.steel <0.5:
			self.servo_msg.data = 0.5304
		elif 0.5 < self.steel: #left
			self.servo_msg.data = 0.15
		elif -0.5 > self.steel:
			self.servo_msg.data = 0.85
		
		self.motor_pub.publish(self.motor_msg)
		self.servo_pub.publish(self.servo_msg)
		rate.sleep()
 

    def joy_callback(self, msg):
	self.speed = msg.axes[1]
	self.steel = msg.axes[2]
	#print(self.speed)
	print(self.steel)

if __name__ == '__main__':
    try:
        test = pure_pursuit()

    except rospy.ROSInterruptException:
        pass
