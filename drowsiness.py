import cv2
import time
import threading
import pygame

class DrowsinessDetector:
    def __init__(self):
        pygame.mixer.init()
        self.faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        self.eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
        self.frame = None
        self.start_time = None
        self.blink_durations = []
        self.DROWSINESS_THRESHOLD = 2.5
        self.calibration_complete = False
        self.alarm_active = False
        self.running = False
        self.mode = None  # 'calibration' or 'monitor'

    def play_alarm(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("static/music.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

    def stop_alarm(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def calibrate(self):
        self.running = True
        self.start_time = None
        self.blink_durations = []
        cap = cv2.VideoCapture(0)
        calibration_start = time.time()
        duration = 15

        while time.time() - calibration_start < duration and self.running:
            ret, img = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                eyes = self.eyeCascade.detectMultiScale(roi, 1.1, 5)
                if len(eyes) == 0:
                    if self.start_time is None:
                        self.start_time = time.time()
                else:
                    if self.start_time:
                        blink_duration = time.time() - self.start_time
                        self.blink_durations.append(blink_duration)
                        self.start_time = None

                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                cv2.putText(img, "Calibrating...", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            self.frame = img

        cap.release()

        if self.blink_durations:
            avg = sum(self.blink_durations) / len(self.blink_durations)
            self.DROWSINESS_THRESHOLD = avg * 2
        else:
            self.DROWSINESS_THRESHOLD = 2.5

        self.calibration_complete = True
        self.running = False
        self.mode = None

    def monitor(self):
        self.running = True
        self.start_time = None
        cap = cv2.VideoCapture(0)

        while self.running:
            ret, img = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.faceCascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                roi = gray[y:y+h, x:x+w]
                eyes = self.eyeCascade.detectMultiScale(roi, 1.1, 5)
                if len(eyes) == 0:
                    if self.start_time is None:
                        self.start_time = time.time()
                    elif time.time() - self.start_time > self.DROWSINESS_THRESHOLD:
                        if not self.alarm_active:
                            self.alarm_active = True
                            threading.Thread(target=self.play_alarm).start()
                        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.putText(img, "DROWSY", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                else:
                    self.start_time = None
                    if self.alarm_active:
                        self.stop_alarm()
                        self.alarm_active = False
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.putText(img, "AWAKE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            self.frame = img

        cap.release()
        self.stop_alarm()
        self.running = False
        self.mode = None

    def generate_video(self):
        while True:
            if self.frame is not None:
                _, jpeg = cv2.imencode('.jpg', self.frame)
                frame_bytes = jpeg.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    def stop(self):
        self.running = False
        self.stop_alarm()
        self.mode = None
