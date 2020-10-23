#!/usr/bin/env python
#from _future_ import print_function

import rospy
from sensor_msgs.msg import LaserScan, PointCloud
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped
from math import cos, sin, pi
from geometry_msgs.msg import Point32

class simple_controller:

    def __init__(self):
        print("ssssss")
        rospy.init_node('simple_controller', anonymous=True)
        #rospy.Subscriber("/scan", LaserScan, self.Laser_callback)
        self.motor_pub = rospy.Publisher('commands/motor/speed', Float64, queue_size= 1)
        self.servo_pub = rospy.Publisher('commands/servo/position', Float64, queue_size= 1)
        self.pcd_pub = rospy.Publisher("laser2pcd", PointCloud, queue_size=1)


        while not rospy.is_shutdown():
            rospy.spin()

    def Laser_callback(self,msg):

        pcd = PointCloud()
        motor_msg = Float64()
        servo_msg=Float64()
        pcd.header.frame_id = msg.header.frame_id
        angle=0

        for r in msg.ranges:
            tmp_point = Point32()
            tmp_point.x = r*cos(angle)
            tmp_point.y = r*sin(angle)
            
            #print(angle, tmp_point.x , tmp_point.y)
            angle = angle+(1.0/180*pi)
            if r<12:
                pcd.points.append(tmp_point)

        count = 0

        for point in pcd.points:
            if point.x >0 and point.x <1 and point.y >-1 and point.y < 1:
                count = count+1

        if count >25:
            motor_msg.data = -2000
            

        else:
            motor_msg.data = 2000 

        #servo_msg.data=0.5304
        
        print(count)
        print("abs")
        self.motor_pub.publish(motor_msg)
        #self.servo_pub.publish(servo_msg)
        self.pcd_pub.publish(pcd)


if __name__ == '__main__':
    try:
        test_track = simple_controller()
    except rospy.ROSInterruptException:
        pass

