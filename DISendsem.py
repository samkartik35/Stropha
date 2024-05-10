import cv2
import serial
import time
import mediapipe as mp

def get_servo_angle(face_center, frame_dimension, servo_max_angle=180):
    """
    Calculate the servo angle to align the face to the center of the frame.

    :param face_center: The coordinate (x or y) of the face center
    :param frame_dimension: The width (for x) or height (for y) of the frame
    :param servo_max_angle: The maximum angle the servo can rotate
    :return: New angle for the servo
    """
    # Calculate the center of the frame
    frame_center = frame_dimension / 2

    # Determine the deviation of the face from the center
    deviation = face_center - frame_center

    # Calculate deviation as a fraction of the total frame dimension
    deviation_fraction = deviation / frame_center

    # Convert fraction to a proportional angle of the servo's range
    angle_change = int((deviation_fraction * (servo_max_angle / 2)))

    # Calculate new servo angle, ensuring it remains within the valid range
    new_angle = max(0, min(servo_max_angle, (servo_max_angle / 2) + angle_change))

    return new_angle

# Initialize serial connection (adjust the COM port as needed)
ser = serial.Serial('COM7', 9600)
time.sleep(2)  # wait for the connection to initialize

# Face detection setup
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

# Hand detection setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

preset_1 = b"90,90\n"
preset_2 = b"80,80\n"
preset_3 = b"100,70\n"

preset_config = {
    1: preset_1,
    2: preset_2,
    3: preset_3
}

preset_mode = 1
live_tracking_mode = False

while True:
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Hand detection
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for landmark in hand_landmarks.landmark:
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmarks.append((cx, cy))
                
            num_fingers = 0
            for finger_tip_id in [4, 8, 12, 16, 20]:
                if landmarks[finger_tip_id][1] < landmarks[finger_tip_id - 2][1]:
                    num_fingers += 1
            
            if num_fingers == 5:
                live_tracking_mode = True
            else:
                live_tracking_mode = False
                if num_fingers in preset_config:
                    preset_mode = num_fingers

    if live_tracking_mode:
    # Live face tracking
        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_center_x = x + w // 2
            face_center_y = y + h // 2
        # Invert pan movement
            pan = get_servo_angle(frame.shape[1] - face_center_x, frame.shape[1])
            tilt = get_servo_angle(face_center_y, frame.shape[0])
            ser.write(f"{pan},{tilt}\n".encode())

    else:
        # Preset modes
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Calculate face center
            face_center_x = (180-(x + w // 2))
            face_center_y = y + h // 2

            # Calculate needed servo angle changes to center the face
            pan = get_servo_angle(face_center_x, frame.shape[1])
            tilt = get_servo_angle(face_center_y, frame.shape[0])

            # Send angles to Arduino
            if preset_mode == 1:
                ser.write(preset_1)
            elif preset_mode == 2:
                ser.write(preset_2)
            elif preset_mode == 3:
                ser.write(preset_3)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
ser.close()
