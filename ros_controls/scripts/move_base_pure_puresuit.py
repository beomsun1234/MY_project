#!/usr/bin/env python
#from _future_ import print_function

import rospy
import rospkg
from sensor_msgs.msg import LaserScan, PointCloud, Imu
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped 
from laser_geometry import LaserProjection
from math import pi, cos, sin , sqrt, pow , atan2
from geometry_msgs.msg import Point32, PoseStamped, Point, PoseWithCovarianceStamped
from nav_msgs.msg import Odometry, Path
import tf



from ackermann_msgs.msg import AckermannDriveStamped

import tf
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class pure_pursuit:
    def __init__(self):
        #rospy.init_node('make_path', anonymous=True)
        #rospy.Subscriber("/move_base/TrajectoryPlannerROS/local_plan",Path, self.path_callback)
  	#rospy.Subscriber("/move_base/TebLocalPlannerROS/local_plan",Path, self.path_callback)
  #/move_base/TebLocalPlannerROS/local_plan
	rospy.Subscriber("/move_base/TebLocalPlannerROS/local_plan",Path, self.path_callback)
        self.motor_pub = rospy.Publisher('commands/motor/speed', Float64, queue_size=1)
        self.servo_pub = rospy.Publisher('commands/servo/position', Float64, queue_size=1)
        self.motor_msg = Float64()
        self.servo_msg = Float64()
	self.stop = 0

        self.is_path = False
        self.forward_point = Point()
        self.current_position = Point()
        self.is_look_forward_point = False
        self.vehicle_length = 0.5
        self.lfd= 0.8
        self.steering = 0
	self.listener = tf.TransformListener()
        self.steering_angle_to_servo_gain = -1.2135
        self.steering_angle_to_servo_offset= 0.5304
	self.servo_msg.data = 0.5304
        rate = rospy.Rate(3)
        while self.stop==0:
            if self.is_path == True:
		try:
			(trans,rot) = self.listener.lookupTransform('/map', '/base_link', rospy.Time(0))
		        amcl_quaternion = (rot[0],rot[1],rot[2],rot[3])
			_,_,self.vehicle_yaw = euler_from_quaternion(amcl_quaternion)
			self.current_position.x = trans[0]
			self.current_position.y = trans[1]

			print(self.current_position.x,self.current_position.y)
			vehicle_position = self.current_position
		        rotated_point = Point()
		        self.is_look_forward_point = False



		        for num, i in enumerate(self.path.poses):
		            path_point = i.pose.position
		            dx = path_point.x - vehicle_position.x
		            dy = path_point.y - vehicle_position.y
		            rotated_point.x = cos(self.vehicle_yaw)*dx +sin(self.vehicle_yaw)*dy
		            rotated_point.y = sin(self.vehicle_yaw)*dx - cos(self.vehicle_yaw)*dy

		            if rotated_point.x>0:
		                dis = sqrt(pow(rotated_point.x,2)+pow(rotated_point.y,2))
		                if dis >= self.lfd:
		                    self.forward_point = path_point
		                    self.is_look_forward_point =True

		                    break            

		        theta = -atan2(rotated_point.y, rotated_point.x)
		        if self.is_look_forward_point:
		            self.steering = atan2((2*self.vehicle_length*sin(theta)), self.lfd)
		            print(self.steering*180/pi)
		            self.motor_msg.data = 2000.0
	    
		        else:
		            self.steering = 0
		            print("no found forward point")
		            self.motor_msg.data = 0
			    self.stop = 1
			    print("Reached!")

			self.motor_pub.publish(self.motor_msg)
		        self.steering_command= (self.steering_angle_to_servo_gain*self.steering)+self.steering_angle_to_servo_offset
		        self.servo_msg.data = self.steering_command		  
		        self.servo_pub.publish(self.servo_msg)

		except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
			print('pose error')
	    if self.stop==1:
		break
            rate.sleep()

    
    def path_callback(self, msg):
        self.is_path = True
        self.path = msg



if __name__ == '__main__':
    try:
        test = pure_pursuit()

    except rospy.ROSInterruptException:
        pass
