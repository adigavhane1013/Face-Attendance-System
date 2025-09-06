Face Recognition Attendance System
This project is a Facial Recognition Attendance System built using Python and OpenCV. It automates attendance marking by recognizing faces in real-time through a webcam, simplifying manual attendance processes.

Features
Real-time face detection and recognition using OpenCV and face_recognition library

Register new users by capturing multiple face images via webcam

Store attendance records with timestamps and save them as CSV files

User-friendly GUI built with Tkinter for easy interaction

Support for viewing, exporting, and managing attendance logs

Modular and scalable design suitable for educational and office use

Technologies Used
Python

OpenCV

face_recognition library

Tkinter (GUI)

NumPy

CSV for attendance record storage

Setup Instructions
Clone or download this repository.

Install required libraries:

bash
pip install opencv-python face_recognition numpy Pillow  
Run the main application file:

bash
python unatt.py  
Use the GUI to register users and start the attendance system.

Folder Structure
Images/ – Stores registered user face images

Attendance/ – Stores attendance CSV files

unatt.py – Main application script

Usage
Register User: Capture at least 5 face images per user for better recognition accuracy.

Start Attendance: Automatically detect and mark attendance for registered users in real-time.

View Records: View and export attendance records to CSV files.

Exit: Close the application safely.

Notes
Ensure your webcam is connected and accessible.

Make sure to install dependencies before running the application.

The system performs best in well-lit environments.
