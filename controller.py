import cv2 
import mediapipe as mp 
import time 
import HandTrackingModule as htm 

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cam_width , cam_height = 1280, 720 

cap = cv2.VideoCapture(0)

cap.set(3,cam_width)
cap.set(4,cam_height)

prev_time = 0 
current_time = 0 
hand_detector = htm.HandDetector(detection_con=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
vol_range = volume.GetVolumeRange()
print(vol_range)
# volume.SetMasterVolumeLevel(-20.0, None)

while True :
	success, img = cap.read()
	current_time = time.time()
	img = cv2.flip(img,1)
	img = hand_detector.find_hands(img)
	lm_list = hand_detector.find_positions(img)
	if len(lm_list) > 0 :

		# For reference : https://google.github.io/mediapipe/solutions/hands.html
		index_finger = lm_list[8]
		thumb_finger = lm_list[4]
		
		x1, y1 = index_finger[1],index_finger[2]
		x2, y2 = thumb_finger[1],thumb_finger[2]
		cx, cy = (x1+x2)//2, (y1+y2)//2 

		cv2.circle(img,(x1,y1),10,(255,255,0),cv2.FILLED)
		cv2.circle(img,(x2,y2),10,(255,255,0),cv2.FILLED)
		cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
		cv2.circle(img,(cx,cy),10,(255,255,0),cv2.FILLED)
		

	fps = 1 / (current_time - prev_time)
	prev_time = current_time
	cv2.putText(img,str(round(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
	
	cv2.imshow("Video Here",img)
	cv2.waitKey(1)


