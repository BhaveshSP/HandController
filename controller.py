# Imports 
import cv2 
import mediapipe as mp 
import time 
import HandTrackingModule as htm 
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np 
import screen_brightness_control as sbc 

# Set the Video Screen Width and Height 
cam_width , cam_height = 1280, 720 
cap = cv2.VideoCapture(0)
cap.set(3,cam_width)
cap.set(4,cam_height)

# Initialization 
prev_time = 0 
current_time = 0
bar = 400 


hand_detector = htm.HandDetector(detection_con=0.8)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get the Volume Range for the System 
vol_range = volume.GetVolumeRange()
min_volume = vol_range[0]
max_volume = vol_range[1]

# Toggle Between Controlling Brightness and Volume 
volume_toggle = False 

while True :
    success, img = cap.read()
    current_time = time.time()
    # Flip the View to give mirror like result 
    img = cv2.flip(img,1)
    # Detect Hand
    img = hand_detector.find_hands(img,False)
    # Get the landmarks list 
    lm_list_one = hand_detector.find_positions(img,0)
    
    if len(lm_list_one) > 0 :
        
        # For reference : https://google.github.io/mediapipe/solutions/hands.html
        
        # Get the coordinates for the Index finger and thumb 
        index_finger = lm_list_one[8]
        thumb_finger = lm_list_one[4]
        x1, y1 = index_finger[1],index_finger[2]
        x2, y2 = thumb_finger[1],thumb_finger[2]
        # Calculate the center of the index finger and thumb 
        cx, cy = (x1+x2)//2, (y1+y2)//2 
        # Draw circle on the index finger tip 
        cv2.circle(img,(x1,y1),10,(255,255,0),cv2.FILLED)
        # Draw circle on the thumb tip
        cv2.circle(img,(x2,y2),10,(255,255,0),cv2.FILLED)
        # Draw line from the index finger tip to thumb tip 
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
        # Draw circle on the center of the index finger and thumb
        cv2.circle(img,(cx,cy),10,(255,255,0),cv2.FILLED)
        
        # Calculate the length between the index finger tip and thumb 
        length = hypot(x2-x1,y2-y1)
        
        # Control the volume 
        if volume_toggle :
            vol = np.interp(length,[20,160],[min_volume,max_volume])
            bar = np.interp(length,[20,100],[400,150])
            volume.SetMasterVolumeLevel(vol,None)
        # Control the brightness 
        else:
            brightness = np.interp(length,[20,160],[0,100])
            bar = np.interp(length,[20,160],[400,150])
            sbc.set_brightness(brightness)
        # Color the center with red if less then minimum length 
        if length < 20:
            cv2.circle(img,(cx,cy),10,(255,0,0),cv2.FILLED) 
        
            
    # Draw a frame for meter 
    cv2.rectangle(img,(50,150),(85,400),(255,0,0),3)
    # Fill the meter 
    cv2.rectangle(img,(50,int(bar)),(85,400),(255,0,0),cv2.FILLED)
    
    # Calculate FPS
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    # Display FPS 
    cv2.putText(img,str(round(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
    cv2.imshow("Video Here",img)
    
    cv2.waitKey(1)
    
    
    
