# this whole file is from OpenCV docs https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html
from __future__ import print_function
import cv2 as cv
import argparse
import numpy

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        #-- In each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)
        for (x2,y2,w2,h2) in eyes:
            eye_center = (x + x2 + w2//2, y + y2 + h2//2)
            radius = int(round((w2 + h2)*0.25))
            frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
    cv.imshow('Capture - Face detection', frame)
parser = argparse.ArgumentParser(description='Code for Cascade Classifier tutorial.')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='examples/haarcascades/haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='examples/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
parser.add_argument('--camera', help='Camera divide number.', type=int, default=0)
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
#-- 1. Load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)
camera_device = args.camera
#-- 2. Read the video stream
cap = cv.VideoCapture(camera_device)
if not cap.isOpened:
    print('--(!)Error opening video capture')
    exit(0)
while True:
    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        break
    detectAndDisplay(frame)
    if cv.waitKey(10) == 27:
        break

        # the code below comes from: https://medium.com/@amit25173/opencv-eye-tracking-aeb4f1b46aa3
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (fx, fy, fw, fh) in faces:
        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        roi_color = frame[fy:fy+fh, fx:fx+fw]
        
        eyes = eyes_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            eye_gray = roi_gray[ey:ey+eh, ex:ex+ew]
            eye_color = roi_color[ey:ey+eh, ex:ex+ew]
            
            # Thresholding to isolate the pupil
            _, thresh = cv.threshold(eye_gray, 50, 255, cv.THRESH_BINARY_INV)
            
            # Find contours
            contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x: cv.contourArea(x), reverse=True)
            print(f"Contours detected: {len(contours)}")
            
            if contours:
                (cx, cy), radius = cv.minEnclosingCircle(contours[0])
                cv.circle(eye_color, (int(cx), int(cy)), int(radius), (255, 0, 0), 2)
                cv.line(frame, (int(cx), int(cy)), (int(cx) + 50, int(cy)), (0, 255, 0), 2)  # Horizontal line
                cv.line(frame, (int(cx), int(cy)), (int(cx), int(cy) + 50), (0, 255, 0), 2)  # Vertical line
                #this part I wrote!!!
                distanceInX = ex-cx
                distanceInY = ey-cy
                print(distanceInX, distanceInY)
    
    cv.imshow('Pupil Detection', frame)
    
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


# def pupilCoordinates():
#     4 = (31-38, 38-48)

cap.release()
cv.destroyAllWindows()