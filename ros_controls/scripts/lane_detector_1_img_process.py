#!/usr/bin/env python

import rospy
import cv2
import numpy as np
import os, rospkg
import json
import time

from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridgeError

from utils_2 import BEVTransform, CURVEFit, draw_lane_img

class IMGParser:
    def __init__(self, currentPath):
        self.img = None
        #region fixed code
        self.cameraFeed = True
        #self.videoPath = currentPath + "/scripts/drive_video/sample_drive.mp4"
        #self.videoPath = currentPath + "/scripts/drive_video/drive.avi"
        #self.videoPath = currentPath + "/scripts/drive_video/drive_dark.avi"
        self.videoPath = currentPath + "/scripts/drive_video/test333.bag"
        self.cameraNo = 1
        self.cameraWidth = 640
        self.cameraHeight = 360
        self.frameWidth = 640
        self.frameHeight = 360
        #endregion
        self.set_cam()
        self.testbar_name = "VariablePanel"
        print(self.videoPath)

    def set_cam(self):
        if self.cameraFeed:
            self.cam = cv2.VideoCapture(self.cameraNo)
            self.cam.set(3, self.cameraWidth)
            self.cam.set(4, self.cameraHeight)
        else:
            self.cam = cv2.VideoCapture(self.videoPath)
        
    def get_image(self):
        ret, image = self.cam.read()

        if not ret:
            self.set_cam()
        else:
            image = cv2.resize(image, (self.frameWidth, self.frameHeight), interpolation = cv2.INTER_AREA)
        
        return ret, image

    def image_process(self, imgMat, src):
        # Apply HLS color filtering to filter out white lane lines
        hlsMat = cv2.cvtColor(imgMat, cv2.COLOR_BGR2HLS)
        
        # lower_white = np.array([src[0], src[1], src[2]])
        lower_white = np.array([210, 90, 194])
        upper_white = np.array([255, 255, 255])
        mask = cv2.inRange(imgMat, lower_white, upper_white)
        imgMat = cv2.bitwise_and(imgMat, hlsMat, mask = mask)
        #return imgMat
        # Convert image to grayscale, apply threshold, blur & extract edges
        imgMat = cv2.cvtColor(imgMat, cv2.COLOR_BGR2GRAY)
        # return imgMat
        # ret, imgMat = cv2.threshold(imgMat, src[0], src[1], cv2.THRESH_BINARY)
        ret, imgMat = cv2.threshold(imgMat, 131, 255, cv2.THRESH_BINARY)
        # return imgMat
        imgMat = cv2.GaussianBlur(imgMat,(3, 3), 0)
        #return imgMat
        # edge
        #imgMat = cv2.Canny(imgMat, 40, 60)
        return imgMat

    #region CODE BLOCK REGION -> IOELECTRON TEST BAR CONTROL
    def TESTbar_nothing(self, x):
        pass

    def initializeTESTbar(self, intialTestbarVals):
        #intializing trackbars for region of intrest
        cv2.namedWindow(self.testbar_name, cv2.WINDOW_NORMAL)
        cv2.createTrackbar("REF1", self.testbar_name, intialTestbarVals[0], 255, self.TESTbar_nothing)
        cv2.createTrackbar("REF2", self.testbar_name, intialTestbarVals[1], 255, self.TESTbar_nothing)
        cv2.createTrackbar("REF3", self.testbar_name, intialTestbarVals[2], 255, self.TESTbar_nothing)
        cv2.createTrackbar("REF4", self.testbar_name, intialTestbarVals[3], 255, self.TESTbar_nothing)
        cv2.resizeWindow(self.testbar_name, 400, 400)

    def readTestVal(self):
        src = []
        src.append(int(cv2.getTrackbarPos("REF1", self.testbar_name)))
        src.append(int(cv2.getTrackbarPos("REF2", self.testbar_name)))
        src.append(int(cv2.getTrackbarPos("REF3", self.testbar_name)))
        src.append(int(cv2.getTrackbarPos("REF4", self.testbar_name)))
        return src
    #endregion

if __name__ == '__main__':
    rp= rospkg.RosPack()

    currentPath = rp.get_path("ros_controls")

    rospy.init_node('lane_detector',  anonymous=True)

    image_parser = IMGParser(currentPath)
    
    initializeTESTbar = [100, 100, 100, 100]
    image_parser.initializeTESTbar(initializeTESTbar)
    src = image_parser.readTestVal()

    prevTime = curTime = time.time()

    while not rospy.is_shutdown():
        curTime = time.time()
        
        fps = 1 / (curTime - prevTime)
        prevTime = curTime
        fps_str = "FPS: %0.1f" % fps

        ret, img_wlane = image_parser.get_image()
        if not ret: continue

        src = image_parser.readTestVal()

        img_wlane = image_parser.image_process(img_wlane, src)

        cv2.putText(img_wlane, fps_str, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
        
        cv2.imshow(image_parser.testbar_name, img_wlane)

        if cv2.waitKey(1) == 13: break
