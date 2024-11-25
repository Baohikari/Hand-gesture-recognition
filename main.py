import cv2
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc
import numpy as np


class BrightnessControl:
    def __init__(self):
        self.cap = None
        self.running = False
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=False,
            model_complexity=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75,
            max_num_hands=2,
        )
        self.draw = mp.solutions.drawing_utils

    def start_camera(self, update_frame_callback):
        self.cap = cv2.VideoCapture(0)
        self.running = True

        while self.running:
            _, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            process = self.hands.process(frameRGB)

            landmarkList = []
            if process.multi_hand_landmarks:
                for handlm in process.multi_hand_landmarks:
                    for _id, landmarks in enumerate(handlm.landmark):
                        height, width, _ = frame.shape
                        x, y = int(landmarks.x * width), int(landmarks.y * height)
                        landmarkList.append([_id, x, y])

                    self.draw.draw_landmarks(
                        frame, handlm, self.mpHands.HAND_CONNECTIONS
                    )

            if landmarkList:
                x_1, y_1 = landmarkList[4][1], landmarkList[4][2]
                x_2, y_2 = landmarkList[8][1], landmarkList[8][2]
                cv2.circle(frame, (x_1, y_1), 7, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x_2, y_2), 7, (0, 255, 0), cv2.FILLED)
                cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 3)
                L = hypot(x_2 - x_1, y_2 - y_1)
                b_level = np.interp(L, [15, 220], [0, 100])
                sbc.set_brightness(int(b_level))
                cv2.putText(
                    frame,
                    f"Brightness: {int(b_level)}%",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

            update_frame_callback(frame)

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
