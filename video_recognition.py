import cv2
import numpy as np
import os
import tkinter as tk
import threading

DATASET_DIR = r"D:\dbms project\pictures"

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

def prepare_training_data(data_dir):
    images = []
    labels = []
    name_to_label = {}
    label_to_name = {}
    current_label = 0

    for person_name in os.listdir(data_dir):
        person_dir = os.path.join(data_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        if person_name not in name_to_label:
            name_to_label[person_name] = current_label
            label_to_name[current_label] = person_name
            current_label += 1

        for img_name in os.listdir(person_dir):
            img_path = os.path.join(person_dir, img_name)
            image = cv2.imread(img_path)

            if image is None:
                continue

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

            if len(faces) == 0:
                continue

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                images.append(face)
                labels.append(name_to_label[person_name])

    return images, labels, label_to_name

root = tk.Tk()
root.title("Patient Info")

label_name = tk.Label(root, text="Name: ")
label_name.grid(row=0, column=0, padx=10, pady=5)

name_var = tk.StringVar()
tk.Label(root, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

def close_app():
    global running
    running = False
    video_capture.release()
    cv2.destroyAllWindows()
    root.destroy()

close_button = tk.Button(root, text="Close", command=close_app)
close_button.grid(row=1, column=0, columnspan=2, pady=10)

images, labels, label_to_name = prepare_training_data(DATASET_DIR)
if len(images) > 0:
    recognizer.train(images, np.array(labels))

video_capture = cv2.VideoCapture(0)
running = True

def recognize_faces():
    global running,name
    while running:
        ret, frame = video_capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            label, confidence = recognizer.predict(face)

            if confidence < 70:
                name = label_to_name[label]
                name_var.set(name)  # Update the name in the GUI

                print(name)  # Print the recognized name to the console
                close_app()  # Close the application after detecting a face

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Face Recognition Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False

    video_capture.release()
    cv2.destroyAllWindows()

recognition_thread = threading.Thread(target=recognize_faces)
recognition_thread.start()

root.mainloop()
