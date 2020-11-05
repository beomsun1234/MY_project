#!/usr/bin/env python
import rospy
import cv2
import numpy as np
import os, rospkg
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridgeError

class Lane_mycar:
    def __init__(self):
        #rospy.init_node('Lane_myCar', anonymous=True)
        self.image_sub = rospy.Subscriber("/usb_cam2/image_raw/compressed/compressed", CompressedImage, self.callback)
        self.motor_pub = rospy.Publisher('commands/motor/speed', Float64, queue_size=1)
        self.servo_pub = rospy.Publisher('commands/servo/position', Float64, queue_size=1)
        self.motor_msg = Float64()
        self.servo_msg = Float64()
        self.steering = 0
        self.ck=0
        self.pix_r=0
        self.block =0
        self.pix_l=0
        self.stopck=0
        self.ack =0
        

    def callback(self, msg):
        try:
            np_arr = np.fromstring(msg.data, np.uint8)
            img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except CvBridgeError as e:
            print(e)
        pix_l = 0
        pix_r = 0
        #img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2HSV)
        l_img = img_bgr[310:430, 68:308] ##roi left
        r_img = img_bgr[310:430:, 308:556] ##roi right
        h = img_bgr.shape[0]
        w = img_bgr.shape[1]
        #print(h) 460
        ch = 308 ## center circle h
        cw = 308 ## cneter circle w
        lh = 68 ## left circle Height 89
        lw = 308## left circle weight
        rh = 556 ## right circle H
        rw = 308 ## right circle H
        ##
        cv2.circle(img_bgr, (ch, cw), 5, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        cv2.circle(img_bgr, (lh, lw), 5, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        cv2.circle(img_bgr, (rh, rw), 5, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        ##
        hlsMat = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HLS)
        l_hlsMat = cv2.cvtColor(l_img, cv2.COLOR_BGR2HLS) 
        r_hlsMat = cv2.cvtColor(r_img, cv2.COLOR_BGR2HLS)
        ##
        lower_white = np.array([210, 90, 194])
        upper_white = np.array([255, 255, 255])
        ##
        cmask = cv2.inRange(img_bgr, lower_white, upper_white)
        lmak = cv2.inRange(l_img, lower_white, upper_white)
        rmak = cv2.inRange(r_img, lower_white, upper_white)

        ##
        imgMat = cv2.bitwise_and(img_bgr, hlsMat, mask = cmask)
        limgMat = cv2.bitwise_and(l_img, l_hlsMat, mask = lmak)
        rimgMat = cv2.bitwise_and(r_img, r_hlsMat, mask = rmak)
        #
        # Convert image to grayscale, apply threshold, blur & extract edges
        imgMat = cv2.cvtColor(imgMat, cv2.COLOR_BGR2GRAY)
        limgMat = cv2.cvtColor(limgMat, cv2.COLOR_BGR2GRAY)
        rimgMat = cv2.cvtColor(rimgMat, cv2.COLOR_BGR2GRAY)
        # -------------------------------------------------
        # ----------------------------------------------------
        ret, imgMat = cv2.threshold(imgMat, 131, 255, cv2.THRESH_BINARY)
        ret, limgMat = cv2.threshold(limgMat, 131, 255, cv2.THRESH_BINARY)
        ret, rimgMat = cv2.threshold(rimgMat, 131, 255, cv2.THRESH_BINARY)
        # Convert GaussianBlur
        imgMat = cv2.GaussianBlur(imgMat,(3, 3), 0)
        limgMat = cv2.GaussianBlur(limgMat,(3, 3), 0)
        rimgMat = cv2.GaussianBlur(rimgMat,(3, 3), 0)
        # edge
        #imgMat = cv2.Canny(imgMat, 40, 60)
        self.pix_l = cv2.countNonZero(limgMat)
        self.pix_r = cv2.countNonZero(rimgMat)
        self.ck = abs(self.pix_l-self.pix_r)
        #print(self.pix_l,self.pix_r)

        if self.ack == 0: 
            #cv2.imshow('imageB', img_bgr)
            self.stop()
            self.controll()
            cv2.waitKey(1)

    def controll(self):
        if self.ck >1550 and self.pix_l> self.pix_r:
            self.steering = 0.10
            self.motor_msg.data = 1000
            print("go right")
        elif self.ck >1550 and self.pix_l<self.pix_r:
            self.steering = 0.90
            self.motor_msg.data = 1000
            print("go right")
        elif self.ck <100:
            print("stop3")
            self.motor_msg.data = 0
            self.steering = 0.5304
            self.stopck = self.stopck+1
        else:
            self.motor_msg.data = 1000
            self.steering = 0.5304


        self.servo_msg.data = self.steering
        self.servo_pub.publish(self.servo_msg)
        self.motor_pub.publish(self.motor_msg)

    def stop(self):
        if self.stopck == 4:
            print("end end end")
            #rospy.signal_shutdown(self.stopck==3)
            self.ack =1
        

    def play(self):
        rate = rospy.Rate(50)
        while self.ack==0:
            self.stop()
            if self.ack==1: break
            rate.sleep()



if __name__ == "__main__":

    print("a")


