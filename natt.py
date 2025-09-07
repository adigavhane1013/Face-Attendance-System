import tkinter as tk
from tkinter import ttk, messagebox, font
import cv2
import os
import sys
import numpy as np
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import subprocess

class FaceAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(True, True)
        
        # Set custom font
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        
        # Create style for ttk widgets
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=self.button_font, background='#0078D7', foreground='white')
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', font=self.normal_font, background='#f0f0f0')
        
        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Face Recognition Attendance System", font=self.title_font)
        self.title_label.pack(pady=20)
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=30, fill=tk.X)
        
        # Buttons with icons
        self.btn_start = tk.Button(self.buttons_frame, text="Start Attendance System", 
                                  font=self.button_font, bg="#0078D7", fg="white",
                                  padx=20, pady=10, borderwidth=0,
                                  command=self.start_attendance_system)
        self.btn_start.pack(pady=10, fill=tk.X)
        
        self.btn_register = tk.Button(self.buttons_frame, text="Register New User", 
                                     font=self.button_font, bg="#107C10", fg="white",
                                     padx=20, pady=10, borderwidth=0,
                                     command=self.register_new_user)
        self.btn_register.pack(pady=10, fill=tk.X)
        
        self.btn_view = tk.Button(self.buttons_frame, text="View Attendance Records", 
                                 font=self.button_font, bg="#5C2D91", fg="white",
                                 padx=20, pady=10, borderwidth=0,
                                 command=self.view_attendance)
        self.btn_view.pack(pady=10, fill=tk.X)
        
        self.btn_exit = tk.Button(self.buttons_frame, text="Exit", 
                                 font=self.button_font, bg="#D83B01", fg="white",
                                 padx=20, pady=10, borderwidth=0,
                                 command=self.exit_app)
        self.btn_exit.pack(pady=10, fill=tk.X)
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Create directories if they don't exist
        if not os.path.exists('Images'):
            os.makedirs('Images')
        if not os.path.exists('Attendance'):
            os.makedirs('Attendance')
    
    def start_attendance_system(self):
        self.status_bar.config(text="Starting attendance system...")
        AttendanceSystemWindow(self.root, self.status_bar)
    
    def register_new_user(self):
        self.status_bar.config(text="Opening registration window...")
        RegisterUserWindow(self.root, self.status_bar)
    
    def view_attendance(self):
        self.status_bar.config(text="Opening attendance records...")
        ViewAttendanceWindow(self.root, self.status_bar)
    
    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.root.destroy()
            sys.exit()

class RegisterUserWindow:
    def __init__(self, parent, status_bar):
        self.parent = parent
        self.status_bar = status_bar
        self.window = tk.Toplevel(parent)
        self.window.title("Register New User")
        self.window.geometry("800x600")
        self.window.configure(bg="#f0f0f0")
        self.window.resizable(True, True)
        
        # Font setup
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        
        # Main frame
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Register New User", font=self.title_font)
        self.title_label.pack(pady=10)
        
        # Input frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(pady=10, fill=tk.X)
        
        # Name input
        self.name_label = ttk.Label(self.input_frame, text="Name:", font=self.normal_font)
        self.name_label.pack(side=tk.LEFT, padx=5)
        
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(self.input_frame, textvariable=self.name_var, font=self.normal_font, width=30)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        self.register_btn = ttk.Button(self.input_frame, text="Take Pictures", command=self.start_capture)
        self.register_btn.pack(side=tk.LEFT, padx=10)
        
        # Video frame
        self.video_frame = ttk.Frame(self.main_frame)
        self.video_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Canvas for video
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="Enter name and click 'Take Pictures'", font=self.normal_font)
        self.status_label.pack(pady=10)
        
        # Control buttons
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=10, fill=tk.X)
        
        self.capture_btn = ttk.Button(self.buttons_frame, text="Capture (Space)", state=tk.DISABLED, command=self.capture_image)
        self.capture_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(self.buttons_frame, text="Save Registration", state=tk.DISABLED, command=self.save_registration)
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = ttk.Button(self.buttons_frame, text="Cancel", command=self.close_window)
        self.cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        # Variables
        self.cap = None
        self.is_running = False
        self.captured_images = []
        self.current_frame = None
        self.capture_thread = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Key bindings
        self.window.bind('<space>', lambda event: self.capture_image())
        self.window.bind('<Escape>', lambda event: self.close_window())
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        
        self.window.transient(parent)
        self.window.grab_set()
    
    def start_capture(self):
        if not self.name_var.get().strip():
            messagebox.showerror("Error", "Please enter a name first!")
            return
            
        name = self.name_var.get().strip()
        if os.path.exists(f'Images/{name}_1.jpg'):
            if not messagebox.askyesno("Warning", f"User '{name}' already exists. Do you want to overwrite?"):
                return
                
        if self.is_running:
            return
            
        self.is_running = True
        self.captured_images = []
        self.capture_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED)
        self.status_label.config(text="Camera initialized. Press 'Capture' or SPACE to take pictures (min 5 recommended)")
        
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam!")
                self.is_running = False
                return
                
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.capture_thread = threading.Thread(target=self.update_frame)
            self.capture_thread.daemon = True
            self.capture_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            self.is_running = False
    
    def update_frame(self):
        while self.is_running:
            try:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    self.window.after(0, lambda: self.status_label.config(text="Error: Could not access webcam!"))
                    self.is_running = False
                    break
                    
                self.current_frame = frame.copy()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                
                if self.is_running and self.window.winfo_exists():
                    self.window.after(0, lambda img=img: self.update_canvas(img))
                
                time.sleep(0.03)
            except Exception as e:
                if self.is_running:
                    print(f"Error in update_frame: {str(e)}")
                time.sleep(0.1)
    
    def update_canvas(self, img):
        if not self.is_running or not self.window.winfo_exists():
            return
            
        try:
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.config(width=img.width, height=img.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.image = imgtk
        except Exception as e:
            print(f"Error in update_canvas: {str(e)}")
    
    def capture_image(self):
        if not self.is_running or self.current_frame is None:
            return
            
        self.captured_images.append(self.current_frame.copy())
        self.status_label.config(text=f"Captured {len(self.captured_images)} images. Take at least 5 from different angles.")
        
        if len(self.captured_images) >= 5:
            self.save_btn.config(state=tk.NORMAL)
    
    def save_registration(self):
        if len(self.captured_images) < 5:
            messagebox.showwarning("Warning", "Please capture at least 5 images!")
            return
            
        name = self.name_var.get().strip()
        
        try:
            if not os.path.exists('Images'):
                os.makedirs('Images')
                
            for file in os.listdir('Images'):
                if file.startswith(f"{name}_") and file.endswith(('.jpg', '.jpeg', '.png')):
                    os.remove(os.path.join('Images', file))
            
            saved_count = 0
            for i, img in enumerate(self.captured_images):
                image_path = f'Images/{name}_{i+1}.jpg'
                cv2.imwrite(image_path, img)
                saved_count += 1
            
            messagebox.showinfo("Success", f"Successfully registered {name} with {saved_count} images!")
            self.status_bar.config(text=f"Registered new user: {name}")
            self.close_window()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save images: {str(e)}")
    
    def close_window(self):
        self.is_running = False
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            
        if hasattr(self, 'capture_thread') and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=1.0)
            
        if self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()

class AttendanceSystemWindow:
    def __init__(self, parent, status_bar):
        try:
            import face_recognition
        except ImportError:
            messagebox.showerror("Error", "The face_recognition library is not installed. Please install it with: pip install face_recognition")
            return
            
        self.parent = parent
        self.status_bar = status_bar
        self.window = tk.Toplevel(parent)
        self.window.title("Attendance System")
        self.window.geometry("900x700")
        self.window.configure(bg="#f0f0f0")
        self.window.resizable(True, True)
        
        # Font setup
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        
        # Main frame
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Face Recognition Attendance System", font=self.title_font)
        self.title_label.pack(pady=10)
        
        # Settings frame
        self.settings_frame = ttk.Frame(self.main_frame)
        self.settings_frame.pack(pady=5, fill=tk.X)
        
        # Tolerance slider
        ttk.Label(self.settings_frame, text="Recognition Tolerance:").pack(side=tk.LEFT, padx=5)
        self.tolerance_var = tk.DoubleVar(value=0.6)
        self.tolerance_slider = ttk.Scale(self.settings_frame, from_=0.4, to=0.7, 
                                         orient=tk.HORIZONTAL, length=200,
                                         variable=self.tolerance_var)
        self.tolerance_slider.pack(side=tk.LEFT, padx=5)
        ttk.Label(self.settings_frame, text="Strict").pack(side=tk.LEFT)
        
        # Video frame
        self.video_frame = ttk.Frame(self.main_frame)
        self.video_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Canvas for video
        self.canvas = tk.Canvas(self.video_frame, bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Attendance log frame
        self.log_frame = ttk.Frame(self.main_frame)
        self.log_frame.pack(pady=10, fill=tk.X)
        
        # Log components
        self.log_label = ttk.Label(self.log_frame, text="Attendance Log:", font=self.normal_font)
        self.log_label.pack(anchor=tk.W)
        
        self.log_text = tk.Text(self.log_frame, height=6, font=("Consolas", 10))
        self.log_text.pack(fill=tk.X, pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        # Control buttons
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=10, fill=tk.X)
        
        self.start_btn = ttk.Button(self.buttons_frame, text="Start Recognition", command=self.start_recognition)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(self.buttons_frame, text="Stop", state=tk.DISABLED, command=self.stop_recognition)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.close_btn = ttk.Button(self.buttons_frame, text="Close", command=self.close_window)
        self.close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Variables
        self.cap = None
        self.is_running = False
        self.recognition_thread = None
        self.known_face_encodings = []
        self.known_face_names = []
        self.marked_attendance = set()
        
        # Load known faces
        self.load_known_faces()
        
        # Window setup
        self.window.transient(parent)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.window.bind('<Escape>', lambda event: self.close_window())
    
    def load_known_faces(self):
        import face_recognition
        
        self.known_face_encodings = []
        self.known_face_names = []
        
        if not os.path.exists('Images'):
            messagebox.showerror("Error", "Images directory not found!")
            return
        
        image_files = [f for f in os.listdir('Images') if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            messagebox.showwarning("Warning", "No registered faces found! Please register users first.")
            return
        
        self.log_message("Loading registered faces...")
        
        for file in image_files:
            try:
                name = file.split('_')[0]
                image_path = os.path.join('Images', file)
                image = face_recognition.load_image_file(image_path)
                
                face_encodings = face_recognition.face_encodings(image)
                if len(face_encodings) > 0:
                    self.known_face_encodings.append(face_encodings[0])
                    self.known_face_names.append(name)
                else:
                    self.log_message(f"Warning: No face found in {file}")
                
            except Exception as e:
                self.log_message(f"Error processing {file}: {str(e)}")
        
        unique_names = set(self.known_face_names)
        self.log_message(f"Loaded {len(self.known_face_encodings)} face images for {len(unique_names)} users")
        
    def start_recognition(self):
        import face_recognition
        
        if self.is_running:
            return
            
        if not self.known_face_encodings:
            messagebox.showwarning("Warning", "No registered faces found!")
            return
            
        self.is_running = True
        self.marked_attendance = set()
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_bar.config(text="Recognition system running...")
        
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.attendance_file = f'Attendance/Attendance-{self.today}.csv'
        
        if not os.path.exists('Attendance'):
            os.makedirs('Attendance')
            
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'w') as f:
                f.write('Name,Time,Date\n')
        
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Error", "Could not open webcam!")
                self.is_running = False
                self.start_btn.config(state=tk.NORMAL)
                self.stop_btn.config(state=tk.DISABLED)
                return
                
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            
            self.recognition_thread = threading.Thread(target=self.run_recognition)
            self.recognition_thread.daemon = True
            self.recognition_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start camera: {str(e)}")
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def run_recognition(self):
        import face_recognition
        
        process_this_frame = True
        frame_count = 0
        
        while self.is_running:
            try:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    self.log_message("Error: Could not access webcam!")
                    break
                    
                if process_this_frame:
                    try:
                        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                        
                        face_locations = face_recognition.face_locations(rgb_small_frame)
                        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                        
                        face_names = []
                        tolerance = self.tolerance_var.get()
                        
                        for face_encoding in face_encodings:
                            matches = face_recognition.compare_faces(
                                self.known_face_encodings, face_encoding, tolerance=tolerance
                            )
                            name = "Unknown"
                            confidence = 0
                            
                            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                            if len(face_distances) > 0:
                                best_match_index = np.argmin(face_distances)
                                confidence = 1 - face_distances[best_match_index]
                                
                                if matches[best_match_index]:
                                    name = self.known_face_names[best_match_index]
                                    
                                    if name not in self.marked_attendance and name != "Unknown":
                                        self.mark_attendance(name)
                                        self.marked_attendance.add(name)
                            
                            face_names.append((name, confidence))
                            
                        display_frame = frame.copy()
                        for (top, right, bottom, left), (name, confidence) in zip(face_locations, face_names):
                            top *= 4
                            right *= 4
                            bottom *= 4
                            left *= 4
                            
                            color = (0, 0, 255) if name == "Unknown" else (0, 255, 0)
                            
                            cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
                            cv2.rectangle(display_frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                            
                            confidence_text = f"{confidence:.2f}" if confidence > 0 else "N/A"
                            text = f"{name} ({confidence_text})"
                            cv2.putText(display_frame, text, (left + 6, bottom - 6), 
                                      cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                    except Exception as e:
                        self.log_message(f"Error in face recognition: {str(e)}")
                        display_frame = frame
                else:
                    display_frame = frame
                
                process_this_frame = not process_this_frame
                
                rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                
                if self.is_running and self.window.winfo_exists():
                    self.window.after(0, lambda img=img: self.update_canvas(img))
                
                frame_count += 1
                time.sleep(0.03)
                
            except Exception as e:
                if self.is_running:
                    self.log_message(f"Error in recognition loop: {str(e)}")
                time.sleep(0.1)
    
    def update_canvas(self, img):
        if not self.is_running or not self.window.winfo_exists():
            return
            
        try:
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.config(width=img.width, height=img.height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.image = imgtk
        except Exception as e:
            print(f"Error in update_canvas: {str(e)}")
    
    def mark_attendance(self, name):
        now = datetime.now()
        time_string = now.strftime('%H:%M:%S')
        date_string = now.strftime('%Y-%m-%d')
        
        self.log_message(f"Marked attendance for {name} at {time_string}")
        
        try:
            with open(self.attendance_file, 'a') as f:
                f.write(f'{name},{time_string},{date_string}\n')
        except Exception as e:
            self.log_message(f"Error writing attendance: {str(e)}")
    
    def log_message(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_text = f"[{timestamp}] {message}\n"
        
        self.window.after(0, self._update_log, log_text)
    
    def _update_log(self, text):
        if not self.window.winfo_exists():
            return
            
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def stop_recognition(self):
        self.is_running = False
        
        if self.cap is not None:
            self.cap.release()
            self.cap = None
            
        if hasattr(self, 'recognition_thread') and self.recognition_thread.is_alive():
            self.recognition_thread.join(timeout=1.0)
            
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_bar.config(text="Recognition system stopped.")
        self.log_message("Recognition system stopped")
    
    def close_window(self):
        if self.is_running:
            self.stop_recognition()
            
        if self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()

class ViewAttendanceWindow:
    def __init__(self, parent, status_bar):
        self.parent = parent
        self.status_bar = status_bar
        self.window = tk.Toplevel(parent)
        self.window.title("View Attendance Records")
        self.window.geometry("800x600")
        self.window.configure(bg="#f0f0f0")
        self.window.resizable(True, True)
        
        # Font setup
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = font.Font(family="Helvetica", size=12)
        
        # Main frame
        self.main_frame = ttk.Frame(self.window)
        self.main_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Attendance Records", font=self.title_font)
        self.title_label.pack(pady=10)
        
        # Controls frame
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.pack(fill=tk.X, pady=10)
        
        # Date selector
        ttk.Label(self.controls_frame, text="Select Date:", font=self.normal_font).pack(side=tk.LEFT, padx=5)
        
        self.attendance_dates = self.get_attendance_dates()
        self.selected_date = tk.StringVar(value=self.attendance_dates[0] if self.attendance_dates else "No records")
        self.date_dropdown = ttk.Combobox(self.controls_frame, textvariable=self.selected_date, 
                                          values=self.attendance_dates, state="readonly", width=20)
        self.date_dropdown.pack(side=tk.LEFT, padx=5)
        
        # View button
        self.view_btn = ttk.Button(self.controls_frame, text="View Records", command=self.load_records)
        self.view_btn.pack(side=tk.LEFT, padx=5)
        
        # Export button
        self.export_btn = ttk.Button(self.controls_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_btn.pack(side=tk.LEFT, padx=5)
        
        # Treeview frame
        self.records_frame = ttk.Frame(self.main_frame)
        self.records_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Scrollbars
        self.scrolly = ttk.Scrollbar(self.records_frame)
        self.scrolly.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.scrollx = ttk.Scrollbar(self.records_frame, orient=tk.HORIZONTAL)
        self.scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.records_tree = ttk.Treeview(self.records_frame, yscrollcommand=self.scrolly.set, 
                                         xscrollcommand=self.scrollx.set)
        
        # Configure scrollbars
        self.scrolly.config(command=self.records_tree.yview)
        self.scrollx.config(command=self.records_tree.xview)
        
        # Configure treeview
        self.records_tree["columns"] = ("Name", "Time", "Date")
        self.records_tree.column("#0", width=0, stretch=tk.NO)
        self.records_tree.column("Name", anchor=tk.W, width=150)
        self.records_tree.column("Time", anchor=tk.CENTER, width=100)
        self.records_tree.column("Date", anchor=tk.CENTER, width=100)
        
        self.records_tree.heading("#0", text="", anchor=tk.W)
        self.records_tree.heading("Name", text="Name", anchor=tk.W)
        self.records_tree.heading("Time", text="Time", anchor=tk.CENTER)
        self.records_tree.heading("Date", text="Date", anchor=tk.CENTER)
        
        self.records_tree.pack(fill=tk.BOTH, expand=True)
        
        # Summary frame
        self.summary_frame = ttk.Frame(self.main_frame)
        self.summary_frame.pack(fill=tk.X, pady=10)
        
        self.summary_label = ttk.Label(self.summary_frame, text="Summary: No records loaded", font=self.normal_font)
        self.summary_label.pack(anchor=tk.W)
        
        # Close button
        self.close_btn = ttk.Button(self.main_frame, text="Close", command=self.close_window)
        self.close_btn.pack(pady=10)
        
        # Load initial records
        if self.attendance_dates:
            self.load_records()
        
        # Window setup
        self.window.transient(parent)
        self.window.grab_set()
        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
    
    def get_attendance_dates(self):
        dates = []
        
        if not os.path.exists('Attendance'):
            return ["No records"]
        
        for file in os.listdir('Attendance'):
            if file.startswith('Attendance-') and file.endswith('.csv'):
                date = file.replace('Attendance-', '').replace('.csv', '')
                dates.append(date)
                
        dates.sort(reverse=True)
        
        if not dates:
            return ["No records"]
            
        return dates
    
    def load_records(self):
        for i in self.records_tree.get_children():
            self.records_tree.delete(i)
            
        selected_date = self.selected_date.get()
        
        if selected_date == "No records":
            self.summary_label.config(text="Summary: No attendance records found")
            return
            
        filename = f'Attendance/Attendance-{selected_date}.csv'
        
        if not os.path.exists(filename):
            self.summary_label.config(text=f"Summary: File not found - {filename}")
            return
            
        try:
            with open(filename, 'r') as f:
                csv_reader = f.readlines()
                
            records = csv_reader[1:]
            unique_names = set()
            
            for i, record in enumerate(records):
                if record.strip():
                    parts = record.strip().split(',')
                    if len(parts) >= 3:
                        name, time, date = parts[0], parts[1], parts[2]
                        self.records_tree.insert("", tk.END, values=(name, time, date), iid=str(i))
                        unique_names.add(name)
            
            self.summary_label.config(text=f"Summary: {len(records)} attendance records, {len(unique_names)} unique attendees")
            self.status_bar.config(text=f"Loaded attendance records for {selected_date}")
        
        except Exception as e:
            self.summary_label.config(text=f"Error loading records: {str(e)}")
    
    def export_to_excel(self):
        selected_date = self.selected_date.get()
        
        if selected_date == "No records":
            messagebox.showinfo("Info", "No records to export")
            return
            
        try:
            try:
                import pandas as pd
            except ImportError:
                if messagebox.askyesno("Missing Dependency", 
                                      "Pandas is required for Excel export. Would you like to install it now?"):
                    self.status_bar.config(text="Installing pandas package...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas", "openpyxl"])
                    import pandas as pd
                else:
                    return
            
            input_file = f'Attendance/Attendance-{selected_date}.csv'
            
            if not os.path.exists(input_file):
                messagebox.showerror("Error", f"File not found: {input_file}")
                return
                
            output_file = f'Attendance/Attendance-{selected_date}.xlsx'
            
            df = pd.read_csv(input_file)
            df.to_excel(output_file, index=False)
            
            messagebox.showinfo("Success", f"Successfully exported to {output_file}")
            self.status_bar.config(text=f"Exported records to Excel: {output_file}")
            
            if messagebox.askyesno("Open Folder", "Would you like to open the containing folder?"):
                folder_path = os.path.abspath('Attendance')
                if sys.platform == 'win32':
                    os.startfile(folder_path)
                elif sys.platform == 'darwin':
                    subprocess.call(['open', folder_path])
                else:
                    subprocess.call(['xdg-open', folder_path])
                    
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def close_window(self):
        if self.window.winfo_exists():
            self.window.grab_release()
            self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceAttendanceApp(root)
    root.mainloop()