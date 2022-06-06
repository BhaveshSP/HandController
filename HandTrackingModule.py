import cv2 
import mediapipe as mp 
import time 


class HandDetector:
	
	def __init__(self,mode=False,max_hands=2,complexity=1,detection_con=0.5,track_con=0.5):
		self.mode = mode 
		self.max_hands = max_hands 
		self.detection_con = detection_con 
		self.track_con = track_con 
		self.complexity = complexity
		self.mp_hands = mp.solutions.hands 
		self.hands = self.mp_hands.Hands(self.mode,self.max_hands,self.complexity,self.detection_con,self.track_con)
		self.mp_draw = mp.solutions.drawing_utils
	
	def find_hands(self,img,draw=True):

		img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(img_rgb)
		if self.results.multi_hand_landmarks:
			for hand_lms in self.results.multi_hand_landmarks:
				if draw:
					self.mp_draw.draw_landmarks(img,hand_lms,self.mp_hands.HAND_CONNECTIONS)
		return img 

	def find_positions(self,img,hand_number=0,draw=True):
		lm_list = [] 
		if self.results.multi_hand_landmarks:
			hand = self.results.multi_hand_landmarks[hand_number]
			if hand :
				for idx, lm in enumerate(hand.landmark):
					h,w,_ = img.shape
					cx, cy = int(lm.x*w), int(lm.y*h)
					lm_list.append([idx, cx, cy])
		return lm_list


# Minimum Code for Running Module 

# def main():

# 	cap = cv2.VideoCapture(0)
# 	prev_time = 0 
# 	current_time = 0 
# 	hand_detector = HandDetector()

# 	while True :
# 		success, img = cap.read()
# 		current_time = time.time()
# 		img = cv2.flip(img,1)
# 		img = hand_detector.find_hands(img)
# 		lm_list = hand_detector.find_positions(img)
# 		if len(lm_list) > 0 :
# 			print(lm_list[0])

# 		fps = 1 / (current_time - prev_time)
# 		prev_time = current_time
# 		cv2.putText(img,str(round(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)
		
# 		cv2.imshow("Video Here",img)
# 		cv2.waitKey(1)




# if __name__ == "__main__":
# 	main()