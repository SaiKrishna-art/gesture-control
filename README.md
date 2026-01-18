Touchless Gesture-Based System Control

This project is a real-time gesture-controlled desktop application that allows users to control system functions such as cursor movement, volume, brightness, and media playback using hand gestures captured through a webcam.

The project demonstrates practical applications of Computer Vision and Human–Computer Interaction (HCI) using Python.

Features

Real-time hand tracking using a webcam

Cursor movement using index finger tracking

Volume control using two-finger vertical hand movement

Brightness control using three-finger vertical hand movement

Media play and pause using open palm gesture

Lock and unlock mechanism to prevent accidental actions

Packaged as a standalone Windows executable

Stabilized and smooth gesture detection

Gesture Mapping
Gesture	Action
Closed fist (hold)	Lock / Unlock system
One finger	Cursor movement
Two fingers + vertical motion	Volume control
Three fingers + vertical motion	Brightness control
Open palm	Play / Pause media
Q / ESC key	Exit application
System Architecture
Webcam
  ↓
OpenCV Frame Processing
  ↓
MediaPipe Hand Landmark Detection
  ↓
Gesture Classification and Stabilization
  ↓
Mode Locking and Cooldown Control
  ↓
System-Level Actions

Technologies Used

Python 3.10

OpenCV

MediaPipe

PyAutoGUI

screen-brightness-control

PyInstaller

Installation (For Development)
Step 1: Clone the repository
git clone https://github.com/your-username/gesture-control.git
cd gesture-control

Step 2: Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate

Step 3: Install dependencies
pip install -r requirements.txt

Step 4: Run the application
python main.py

Building the Executable (Windows)
pyinstaller --onefile --windowed --add-data ".venv\Lib\site-packages\mediapipe;mediapipe" --add-data ".venv\Lib\site-packages\cv2;cv2" --hidden-import=cv2 --hidden-import=mediapipe --name GestureControl main.py


The executable will be generated in:

dist/GestureControl.exe

Usage Instructions

Run the application

Allow webcam access when prompted

Unlock the system using the closed-fist gesture (hold for one second)

Perform gestures to control the system

Press Q or ESC to exit the application

For best performance, ensure good lighting and keep your hand clearly visible in front of the camera.

Limitations

Requires adequate lighting for reliable detection

Supports single-hand gestures only

Brightness control may require administrator permissions on some systems

Performance depends on webcam quality and system resources

Future Enhancements

Custom gesture training using machine learning

Multi-hand gesture support

Voice and gesture hybrid interaction

Cross-platform support for Linux and macOS

Mobile camera integration

Academic Relevance

This project is suitable for:

Final-year engineering projects

Computer Vision coursework

Human–Computer Interaction (HCI) studies

AI and Data Science portfolios

License

This project is intended for educational purposes.
Users are free to modify and extend the code for learning and research.

Acknowledgements

OpenCV community

MediaPipe development team

Python Software Foundation


