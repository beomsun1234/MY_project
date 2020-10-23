#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import rospy
from sensor_msgs.msg import LaserScan,PointCloud
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped
from math import cos,sin,pi
from geometry_msgs.msg import Point32

class simple_controller:
    def __init__(self):
        #rospy.init_node('simple_controller',anonymous=True)
        rospy.Subscriber("/scan",LaserScan,self.laser_callback)
        self.motor_pub = rospy.Publisher('commands/motor/speed',Float64,queue_size=1)
        self.servo_pub = rospy.Publisher('commands/servo/position',Float64,queue_size=1)
        self.pcd_pub = rospy.Publisher('laser2pcd',PointCloud,queue_size=1)

	self.switch = 0
	self.left = 0 
        self.stop = 1
	self.back = 0
	self.ck = 0
        print("simple controller")

        while not rospy.is_shutdown():
	    if self.ck == 1: break
            rospy.spin()

    def laser_callback(self,msg):
        pcd = PointCloud()
        motor_msg = Float64()
        servo_value = Float64()
        pcd.header.frame_id = msg.header.frame_id
        angle = 0

        for r in msg.ranges:
            tmp_point= Point32()
            tmp_point.x = r*cos(angle)
            tmp_point.y = r*sin(angle)
            angle = angle + (1.0/180*pi)
            if r<2 :
                pcd.points.append(tmp_point)
        count_right = 0
        count_left = 0
        max_front = 0
        point_get = []

        for pd in range(0, 360):
            if str(msg.ranges[pd]) == 'inf':
                point_get.append(float(0.0))
            else:
                point_get.append(float(msg.ranges[pd]))

        for point in pcd.points:
            if point.x >0 and point.x<0.3 and point.y>0 and point.y<1:
                count_right = count_right +1
            
            # left
            if point.x >0 and point.x< 0.3 and point.y>-1 and point.y<0: 
                count_left = count_left +1

        # front
        if point_get[179] > point_get[180] and point_get[179] > point_get[181]:
            max_front = point_get[179]
        elif point_get[180] > point_get[179] and point_get[180] > point_get[181]:
            max_front = point_get[180]
        elif point_get[181] > point_get[179] and point_get[181] > point_get[180]:
            max_front = point_get[181]
        print("max_front : ", max_front)
        
        #servo_value = 0.5304
        count = count_left + count_right 
        print("left : " , count_left)
        print("right : " , count_right)
        print("count : ", count)
        print("switch : ", self.switch)
	#print("stop : ", self.stop)
	print("abs:", abs(count_left - count_right))

    	if max_front == 0:
        	motor_msg.data = 0
                print("000000000000000000000000000000000000000000000000")
  
        if self.switch == 0 and self.stop == 1:
	    print("1")
                
            if self.back == 0: 
                servo_value = 0.15
                motor_msg.data = 1000
                self. left = 1

            if 0.3 < max_front < 0.36 and self.left == 1 and self.back == 0:
		print("back")
                self.back = 1
            
            if self.back == 1 :
                if max_front < 0.5:
                    servo_value = 1.0
                elif max_front > 0.5:
                    self.switch = 1
            
                motor_msg.data = -1000 

          
        elif self.switch == 1 and self.stop == 1:
            print("*****************")
	    print("2")
            
	    if  count_right > 35:
		print("comecome!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
		servo_value= 0.5304
	    elif count_right < 35 :
		servo_value = 0.15
	
            motor_msg.data = 1000
	    
	    if 0 < max_front  < 0.38:
		print("stop??????????????????????????????????????????????????????????")
        	servo_value = 0.5304
		motor_msg.data = 0
		self.ck = 1
		self.stop = 0 

        #     if back < 5 and count >= 50:
		# print("back")
		# back = back + 1
	    #     if count_left > count_right : 
        # 		servo_value = 0.85
        # 	else : 
        # 	        servo_value = 0.15
        #     elif back > 5 and count >= 70:
        #   	print("back")
		# back = back + 1
	    #     if count_left > count_right : 
        # 		servo_value = 0.85
        # 	else : 
        # 		servo_value = 0.15
        #         #motor_msg.data = -1000 
	#if self.stop == 1:
	#	servo_value = 0.5304
	#motor_msg.data = 0 

        print("------")
        print(motor_msg.data)
	print(servo_value)
        self.motor_pub.publish(motor_msg)
        self.servo_pub.publish(servo_value)
        self.pcd_pub.publish(pcd)


if __name__ == '__main__':
    try:
        test_track = simple_controller()

    except rospy.ROSInterruptException:
        pass
