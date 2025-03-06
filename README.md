Virtual Mouse Using Hand Tracking
📝 Description

This project implements a Virtual Mouse application using Python, MediaPipe, and OpenCV. The application allows users to control their computer cursor and perform clicks using hand gestures. The hand-tracking functionality is achieved using MediaPipe's hand-tracking capabilities, which detect hand landmarks and translate them into cursor movements and clicks.

🌟 Features

Control the cursor using hand gestures.
Perform clicks by pinching the thumb and index finger.
User-friendly GUI for easy interaction.
Packaged as a standalone executable for cross-platform use.
🛠️ Installation

Prerequisites

Python 3.x
Virtual Environment (optional but recommended)
📦 Packaging the Application

To package the application as a standalone executable, follow these steps:

Install PyInstaller: pip install pyinstaller

Generate the Executable:

pyinstaller --onefile --noconsole \
--add-data "path/to/mediapipe/modules/palm_detection/palm_detection_full.tflite;mediapipe/modules/palm_detection" \
--add-data "path/to/mediapipe/modules/hand_landmark/hand_landmark_full.tflite;mediapipe/modules/hand_landmark" \
--add-data "path/to/mediapipe/modules/hand_landmark/hand_landmark_tracking_cpu.binarypb;mediapipe/modules/hand_landmark" \
virtualMouse.py
Locate the Executable:
The executable will be located in the dist directory.

🖱️ Create a Desktop Shortcut

🚀 Usage
Run the Executable:
Double-click the virtualMouse.exe file to start the application.
Use your index finger to move the cursor.
Pinch your thumb and index finger to click.
