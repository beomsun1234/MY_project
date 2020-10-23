#!/usr/bin/env python
#from _future_ import print_function

import rospy
from sensor_msgs.msg import LaserScan, Imu
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped
from laser_geometry import LaserProjection
from math import cos, sin, pi
from geometry_msgs.msg import Point32
from nav_msgs.msg import Odometry
import tf
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class imu_odom:
    
    def __init__(self):
        rospy.init_node('imu_odom', anonymous=True)
        rospy.Subscriber("/sensors/core", VescStateStamped, self.status_callback)
        rospy.Subscriber("/imu", Imu, self.imu_callback)

        self.is_speed = False
        self.is_imu = False
        

        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=1)
        self.odom_msg = Odometry()
        self.odom_msg.header.frame_id = '/odom'

        self.rpm_gain = 4614
        self.thata = 0

        rate = rospy.Rate(50)

        while not rospy.is_shutdown():

            if self.is_imu ==True and self.is_speed == True:
                print(self.speed, self.thata*180/pi)

                self.thata+=self.yaw_vel*0.05
                x_dot = self.speed*cos(self.thata)/50
                y_dot = self.speed*sin(self.thata)/50

                self.odom_msg.pose.pose.position.x = self.odom_msg.pose.pose.position.x + x_dot
                self.odom_msg.pose.pose.position.y = self.odom_msg.pose.pose.position.y + y_dot
                quaternion = quaternion_from_euler(0,0,self.thata)
                self.odom_msg.pose.pose.orientation.x = quaternion[0]
                self.odom_msg.pose.pose.orientation.y = quaternion[1]
                self.odom_msg.pose.pose.orientation.z = quaternion[2]
                self.odom_msg.pose.pose.orientation.w = quaternion[3]

                self.odom_msg.pose.covariance[0]  = 0.05;
		self.odom_msg.pose.covariance[7]  = 0.05;
		self.odom_msg.pose.covariance[14] = 0.06;
		self.odom_msg.pose.covariance[21] = 0.03;
		self.odom_msg.pose.covariance[28] = 0.03;
		self.odom_msg.pose.covariance[35] = 0.06;

                self.odom_msg.twist.covariance[0]  = 1e-9;
		self.odom_msg.twist.covariance[7]  = 1e-9;
		self.odom_msg.twist.covariance[14] = 1e-9;
		self.odom_msg.twist.covariance[21] = 1e-9;
		self.odom_msg.twist.covariance[28] = 1e-9;
		self.odom_msg.twist.covariance[35] = 1e-9;
	       
		
		self.odom_msg.twist.covariance = self.odom_msg.pose.covariance
                
        
		print(self.odom_msg.pose.covariance)
                self.odom_pub.publish(self.odom_msg)
                br = tf.TransformBroadcaster()
                br.sendTransform((self.odom_msg.pose.pose.position.x, self.odom_msg.pose.pose.position.y, self.odom_msg.pose.pose.position.z), quaternion, rospy.Time.now(),"base_link","odom")
            rate.sleep()


    def status_callback(self,msg):
        self.is_speed =True
        rpm = msg.state.speed
        self.speed = rpm/self.rpm_gain


    def imu_callback(self, msg):
        self.odom_msg.header.stamp= rospy.Time.now()
        self.yaw_vel=msg.angular_velocity.z
        imu_quaternation= (msg.orientation.x, msg.orientation.y, msg.orientation.z,  msg.orientation.w)
        if self.is_imu ==False:
            self.is_imu = True
            _,_,self.thata_offset = euler_from_quaternion(imu_quaternation)
	else:
            _,_,raw_theta = euler_from_quaternion(imu_quaternation)
            self.thata = raw_theta-self.thata_offset
    

if __name__ == "__main__":
    try:
        test = imu_odom()
    except rospy.ROSInterruptException:
        pass


