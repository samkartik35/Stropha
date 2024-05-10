Face and Gesture Tracking Servo Control System
This system utilizes computer vision to perform face tracking and gesture recognition, controlling servo motors accordingly. The application runs on Python, leveraging OpenCV for face detection and MediaPipe for hand gesture recognition. Servo positions are controlled via an Arduino based on the recognized input from the camera feed.

Project Features
Face Tracking: Dynamically track the face within the camera's view and adjust servo positions to keep the face centered.
Gesture Recognition: Detects the number of fingers shown to the camera and switches between different presets or activates face tracking.
Servo Control: Sends angle adjustments to the Arduino to move servos based on face position or preset configurations.
Components
Computer with Python 3.10 and necessary libraries installed.
USB webcam or integrated camera.
Arduino Uno or any compatible microcontroller.
At least two servo motors.
Suitable wires and possibly a breadboard for connections.
External power supply for servo motors (recommended for better performance).
Software Requirements
Python 3.10
OpenCV-Python
MediaPipe
PySerial
Install the required Python packages using pip:

bash
Copy code
pip install opencv-python mediapipe pyserial
Setup and Configuration
Arduino Setup:
Connect the servos to the Arduino according to the pin configuration in your script.
Upload the standard servo control sketch to the Arduino.
Python Script:
Ensure the serial port in the script matches the one used by your Arduino.
Adjust servo maximum angle and other parameters as per your setup requirements.
Running the Application:
Ensure the Arduino is connected to the PC.
Run the Python script to start the application:
bash
Copy code
python face_and_gesture_tracking.py
Usage:

Show your face to the camera; the system will try to center it using the servos.
Change the mode by showing a specific number of fingers:
1 Finger: Activate Preset 1.
2 Fingers: Activate Preset 2.
3 Fingers: Activate Preset 3.
5 Fingers: Switch to live face tracking mode.
Troubleshooting
Serial Port Error: Make sure the Arduino is properly connected and the correct port is specified in the script.
Camera Access: Ensure no other application is using the camera.
Performance Issues: Adjust the detection confidence thresholds if the system is either too sensitive or not sensitive enough.
Contributing
Contributions to the project are welcome! Please fork the repository and submit a pull request with your enhancements.

Kartik- currently has written 100000000000% of the code and made the project
Devesh- data gathering about the project
Tejas- Design and part creation (emotional support as well)

License
This project is open-sourced under the MIT license. Feel free to use it and adapt it as you see fit.
