import cv2
import mediapipe as mp
import numpy as np
import math
import time

class PhysicsThread:
    def __init__(self, segments=12, length=200):
        self.num_segments = segments
        self.segment_len = length / segments
        self.points = np.zeros((segments, 4), dtype=float)
        self.gravity = 0.5  
        self.friction = 0.98 

    def update(self, start_anchor, end_anchor):
        self.points[0, :2] = start_anchor
        self.points[-1, :2] = end_anchor

        for i in range(1, self.num_segments - 1):
            x, y, px, py = self.points[i]
            vel_x = (x - px) * self.friction
            vel_y = (y - py) * self.friction
            
            self.points[i, 2:] = [x, y]
            self.points[i, 0] += vel_x
            self.points[i, 1] += vel_y + self.gravity

        for _ in range(2):
            for i in range(self.num_segments - 1):
                p1 = self.points[i, :2]
                p2 = self.points[i+1, :2]
                dist = math.dist(p1, p2)
                if dist == 0: continue
                
                diff = (self.segment_len - dist) / dist * 0.5
                offset = (p1 - p2) * diff
                
                if i != 0:
                    self.points[i, :2] += offset
                if i+1 != self.num_segments - 1:
                    self.points[i+1, :2] -= offset

    def get_points(self):
        return self.points[:, :2].astype(np.int32)

WIDTH, HEIGHT = 1280, 720
finger_threads = [PhysicsThread(segments=15, length=400) for _ in range(5)]
tips_indices = [4, 8, 12, 16, 20]

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    model_complexity=1,
    min_detection_confidence=0.7, 
    min_tracking_confidence=0.7
)

def draw_glowing_rope(img, points, color, tick):
    pulse = (math.sin(tick * 0.2) + 1) * 2
    cv2.polylines(img, [points], False, color, int(2 + pulse), cv2.LINE_AA)
    cv2.polylines(img, [points], False, (255, 255, 255), 1, cv2.LINE_AA)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1) 
cap.set(cv2.CAP_PROP_EXPOSURE, -4) 

tick = 0
while cap.isOpened():
    success, frame = cap.read()
    if not success: break
    frame = cv2.flip(frame, 1)
    tick += 1
    
    frame_prepped = cv2.convertScaleAbs(frame, alpha=1.3, beta=10)
    
    rgb = cv2.cvtColor(frame_prepped, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hand_data = {'Left': None, 'Right': None}
    if results.multi_hand_landmarks and results.multi_handedness:
        for res_idx, handedness in enumerate(results.multi_handedness):
            label = handedness.classification[0].label
            landmarks = results.multi_hand_landmarks[res_idx]
            hand_data[label] = [(int(lm.x * WIDTH), int(lm.y * HEIGHT)) for lm in landmarks.landmark]

    if hand_data['Left'] and hand_data['Right']:
        for i, tip_idx in enumerate(tips_indices):
            l_tip = hand_data['Left'][tip_idx]
            r_tip = hand_data['Right'][tip_idx]
            
            finger_threads[i].update(np.array(l_tip), np.array(r_tip))
            color = (255, 0, 255) if i == 0 else (255, 255, 0)
            draw_glowing_rope(frame, finger_threads[i].get_points(), color, tick)
    
    cv2.imshow('RTX Neural Physics Threads', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()