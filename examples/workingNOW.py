import cv2
import numpy as np

# Load cascades
face_cascade = cv2.CascadeClassifier('examples/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('examples/haarcascades/haarcascade_eye.xml')

# Parameters for blob detection
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector = cv2.SimpleBlobDetector_create(detector_params)

def cut_eyebrows(img):
    height, _ = img.shape[:2]
    eyebrow_h = int(height / 4)
    return img[eyebrow_h:, :]  # Cut eyebrows out

def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)
    return keypoints

def detect_faces(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = classifier.detectMultiScale(gray_frame, 1.3, 5)
    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])  # Get the largest face
        return img[y:y+h, x:x+w]
    return None

def detect_eyes(img, classifier):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = classifier.detectMultiScale(gray_frame, 1.3, 5)
    height, width = img.shape[:2]
    left_eye, right_eye = None, None
    

    for (x, y, w, h) in eyes:
        eye_region = img[y:y+h, x:x+w]
        gray_eye = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
        blurred_eye = cv2.GaussianBlur(gray_eye, (7, 7), 0)
        _, threshold_eye = cv2.threshold(blurred_eye, 30, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(threshold_eye, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            (cx, cy), radius = cv2.minEnclosingCircle(largest_contour)
            pupil_center = (int(cx), int(cy))

            # Relative position
            relative_x = cx / eye_region.shape[1]
            relative_y = cy / eye_region.shape[0]

            print(f"Pupil relative position: x={relative_x:.2f}, y={relative_y:.2f}")

            # Determine gaze
            if relative_x < 0.6:
                print("Looking left")
            elif relative_x > 0.8:
                print("Looking right")
            else:
                print("Looking center")

        if y > height / 2:
            continue  # Skip detections below the midpoint of the face
        eye_center = x + w / 2
        if eye_center < width / 2:
            left_eye = img[y:y+h, x:x+w]
        else:
            right_eye = img[y:y+h, x:x+w]
    return left_eye, right_eye

def nothing(x):
    pass

def main():
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('image')
    cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error accessing the camera.")
            break

        face_frame = detect_faces(frame, face_cascade)
        if face_frame is not None:
            eyes = detect_eyes(face_frame, eye_cascade)
            for eye in eyes:
                if eye is not None:
                    threshold = cv2.getTrackbarPos('threshold', 'image')
                    eye = cut_eyebrows(eye)
                    keypoints = blob_process(eye, threshold, detector)
                    eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
