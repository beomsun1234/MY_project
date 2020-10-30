#!/usr/bin/env python
import rospy
import cv2
import numpy as np
import os, rospkg
from std_msgs.msg import Float64
from vesc_msgs.msg import VescStateStamped
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridgeError

class IMGParser:
    def __init__(self):

        self.image_sub = rospy.Subscriber("/image_jpeg/compressed", CompressedImage, self.callback)
        self.motor_pub = rospy.Publisher('commands/motor/speed', Float64, queue_size=1)
        self.servo_pub = rospy.Publisher('commands/servo/position', Float64, queue_size=1)
        self.motor_msg = Float64()
        self.servo_msg = Float64()
        self.steering = 0

    def callback(self, msg):
        try:
            np_arr = np.fromstring(msg.data, np.uint8)
            img_bgr = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        except CvBridgeError as e:
            print(e)

        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_RGB2HSV)
        h = img_bgr.shape[0]
        w = img_bgr.shape[1]
        #print(h) 460
        ch = 308
        cw = 325

        lh = 89
        lw = 325

        rh = 521
        rw = 325


        #print(h/3)
        lower_sig_y = np.array([88,7,255])
        upper_sig_y = np.array([90,8,255])
        lower_sig_r = np.array([0,200,200])
        upper_sig_r = np.array([20,255,255])
        lower_sig_g = np.array([50,200,200])
        upper_sig_g = np.array([70,255,255])
        lower_wlane = np.array([0, 0, 200])
        upper_wlane = np.array([100, 50, 255])
        
        #img_l = cv2.Range(327, 460), Range(90, 308)
        #i#mg_r = cv2.Range(327, 460), Range(308, 521)
        dst = img_hsv.copy()
        lx, ly = 310, 56
        lha, lwa = 460, 308
        subimg = dst[lx:lx+lha, ly:ly+lwa]
        #print(lx,ly)
        rx, ry = 310, 578
        rha, rwa = 460, 308
        subimg2 = dst[rx:rx+rha, ry:ry+rwa]
        #print(lx,ly)
        
        cv2.circle(img_bgr, (ch, cw), 5, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        cv2.circle(img_bgr, (lh, lw), 5, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        cv2.circle(img_bgr, (rh, rw), 5, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        #cv2.circle(src, (300, 300), 50, (0, 255, 0), cv2.FILLED, cv2.LINE_4)
        img_l = cv2.inRange(subimg, lower_wlane, upper_wlane)
        img_r = cv2.inRange(subimg2, lower_wlane, upper_wlane)
        img_wlane = cv2.inRange(img_hsv, lower_wlane, upper_wlane)
        #print(img_l)
        ##left
        pix_l = cv2.countNonZero(img_l)
        pix_r = cv2.countNonZero(img_r)
        ck = abs(pix_l-pix_r)
        print(pix_l,pix_r)
        if ck >1550 and pix_l> pix_r:
            self.steering = 0.90
            self.motor_msg.data = 2000
            print("go right")
        elif ck >1550 and pix_l<pix_r:
            self.steering = 0.10
            self.motor_msg.data = 2000
            print("go right")
        else:
            self.motor_msg.data = 2000
            self.steering = 0.5304

        self.servo_msg.data = self.steering
        self.servo_pub.publish(self.servo_msg)
        self.motor_pub.publish(self.motor_msg)
        
        
        #img_wlane = cv2.cvtColor(img_wlane, cv2.COLOR_GRAY2BGR)
        

        #img_concat = np.concatenate([img_r,img_y, img_g], axis=1)

        #cv2.namedWindow('mouseRGB')
        #cv2.imshow('mouseRGB', img_wlane)
        
        #cv2.setMouseCallback('mouseRGB', self.mouseRGB)

        #img_concat = np.concatenate([img_bgr,img_hsv], axis=1)
        cv2.imshow('mouseRGB', img_bgr)
        cv2.imshow("Image L", subimg2)
        cv2.imshow("Image R", subimg)

        cv2.waitKey(1)
    def mouseRGB(self, event, x,y,flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            colorsB = self.img_hsv[y,x,0]
            colorsG = self.img_hsv[y,x,1]
            colorsR = self.img_hsv[y,x,2]
            colors = self.img_hsv[y,x]
            print("red: ",colorsR)
            print("Green: ", colorsG)
            print("Blue: ", colorsB)
            print("BGR Format: ", colors)
            print("Coordinages of pixel: X",x ,"Y: ",y)


if __name__ == "__main__":

    rospy.init_node('image_parser', anonymous=True)

    image_parser = IMGParser()
    rospy.spin()
