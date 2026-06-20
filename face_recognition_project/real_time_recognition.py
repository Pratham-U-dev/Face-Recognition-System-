# real_time_recognition.py

import cv2
import face_recognition
import pickle

ENCODINGS_FILE = "known_faces.dat"

# Load known face data
print("[INFO] Loading known faces...")
with open(ENCODINGS_FILE, "rb") as f:
    known_names, known_encodings = pickle.load(f)
print(f"[INFO] Loaded {len(known_names)} known faces.")

# Start webcam
print("[INFO] Starting webcam. Press 'q' to quit.")
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("[ERROR] Failed to grab frame from webcam.")
        break

    # Resize frame for speed
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect face locations
    face_locations = face_recognition.face_locations(rgb_small_frame)

    try:
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    except Exception as e:
        print(f"[WARNING] Skipping frame: {e}")
        continue

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]

        # Scale face locations back to original size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw rectangle and name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

    cv2.imshow("Face Recognition", frame)

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
