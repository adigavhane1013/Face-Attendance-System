
Face Recognition Attendance System is an innovative Python-based desktop application designed to simplify and automate the process of attendance tracking using real-time face recognition technology. It offers a touchless and efficient alternative to traditional manual or biometric systems by leveraging a webcam and advanced facial recognition libraries.

At its core, the system allows users to **register themselves by capturing face images** through the webcam. Each user is required to take at least five face images from different angles to ensure accurate recognition. These images are then stored locally and used to build a facial database. During registration, the application uses OpenCV to detect faces and saves the captured images into an organized folder structure for future reference.

Once the registration is complete, the attendance module  can be activated. The system starts the webcam and begins scanning for faces in real time. Using the powerful `face_recognition` library, the application compares detected faces with the stored images of registered users. If a match is found, the system marks attendance automatically by logging the user's name, along with the current date and time, into a CSV file. Each user’s attendance is marked only once per session to avoid duplication.

The system also includes a **built-in attendance viewer**, allowing users to review past records. Users can select a specific date to view who was present on that day, and optionally, export the data into an Excel file with a single click. This feature is powered by the Pandas and Openpyxl libraries, making it easy to generate reports and analyze attendance data.

The entire user interface is built using **Tkinter**, Python’s standard GUI library, providing a clean, interactive, and responsive experience. With well-labeled buttons and real-time status updates, the application ensures ease of use even for non-technical users.

This project is ideal for **small institutes, classrooms, or offices** looking for a lightweight yet effective attendance solution. It showcases practical implementation of computer vision and machine learning in a user-friendly environment, making it a great portfolio project for students and developers alike.

