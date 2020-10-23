#!/usr/bin/env python
#from _future_ import print_function

import rospy
from sensor_msgs.msg import LaserScan, Imu
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped,VescState
from laser_geometry import LaserProjection
from math import cos, sin, pi
from geometry_msgs.msg import Point32
from nav_msgs.msg import Odometry
import tf
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import PoseWithCovarianceStamped


class imu_odom:
    
    def __init__(self):
        rospy.init_node('imu_odom', anonymous=True)
        rospy.Subscriber("/sensors/core", VescStateStamped, self.status_callback)
	#rospy.Subscriber("/vesc/commands/motor/speed", Float64, self.speed_callback)
        rospy.Subscriber("/imu", Imu, self.imu_callback)

        self.is_speed = True
        self.is_imu = False
        

        self.odom_pub = rospy.Publisher('/odom', Odometry, queue_size=1)
        self.odom_msg = Odometry()
        self.odom_msg.header.frame_id = '/odom'

        self.rpm_gain = 4614
        self.thata = 0

        rate = rospy.Rate(20)

        while not rospy.is_shutdown():

            if self.is_imu ==True:
                #print(self.speed, self.thata*180/pi)


                x_dot = self.speed*cos(self.thata)/20
                y_dot = self.speed*sin(self.thata)/20

		#print(y_dot)

                self.odom_msg.pose.pose.position.x = self.odom_msg.pose.pose.position.x + x_dot
                self.odom_msg.pose.pose.position.y = self.odom_msg.pose.pose.position.y + y_dot
		#print(self.odom_msg.pose.pose.position.x, self.odom_msg.pose.pose.position.y)
 		#self.odom_msg.pose.covariance = self.corv
		print(self.odom_msg.pose.covariance)
                quaternion = quaternion_from_euler(0,0,self.thata)
                self.odom_msg.pose.pose.orientation.x = quaternion[0]
                self.odom_msg.pose.pose.orientation.y = quaternion[1]
                self.odom_msg.pose.pose.orientation.z = quaternion[2]
                self.odom_msg.pose.pose.orientation.w = quaternion[3]
		self.odom_msg.pose.covariance = [0.1, 0, 0, 0, 0, 0,
						 0, 0.1, 0, 0, 0, 0,
						 0, 0, 0.1, 0, 0, 0,
						 0, 0, 0, 1e6, 0, 0,
						 0, 0, 0, 0, 1e6, 0,
						 0, 0, 0, 0, 0, 0.2]
		print(self.odom_msg.pose.covariance)
		
		self.odom_msg.twist.covariance = [0.1, 0, 0, 0, 0, 0,
						 0, 0.1, 0, 0, 0, 0,
						 0, 0, 0.1, 0, 0, 0,
						 0, 0, 0, 1e6, 0, 0,
						 0, 0, 0, 0, 1e6, 0,
						 0, 0, 0, 0, 0, 0.2]


                self.odom_pub.publish(self.odom_msg)
                br = tf.TransformBroadcaster()
                br.sendTransform((self.odom_msg.pose.pose.position.x, self.odom_msg.pose.pose.position.y, self.odom_msg.pose.pose.position.z), quaternion, rospy.Time.now(),"base_link","odom")
            rate.sleep()


    def status_callback(self,msg):
        self.is_speed =True
        rpm = msg.state.speed
        self.speed = rpm/self.rpm_gain
    
    def speed_callback(self, msg):
	rpm = msg.data
	self.speed = rpm/self.rpm_gain
	


    def imu_callback(self, msg):
        imu_quaternation= (msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w)
        if self.is_imu ==False:
            self.is_imu = True
            _,_,self.thata_offset = euler_from_quaternion(imu_quaternation)
        else:
            _,_,raw_theta = euler_from_quaternion(imu_quaternation)
            self.thata = raw_theta-self.thata_offset
        self.corv = msg.linear_acceleration_covariance
	#print(self.corv)


if __name__ == "__main__":
    try:
        test = imu_odom()
    except rospy.ROSInterruptException:
        pass



