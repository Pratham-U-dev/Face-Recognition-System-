# encode_faces.py

import os
import face_recognition
import pickle

KNOWN_FACES_DIR = "known_faces"
ENCODINGS_FILE = "known_faces.dat"

known_names = []
known_encodings = []

print("[INFO] Encoding faces...")

for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        name = os.path.splitext(filename)[0]
        image_path = os.path.join(KNOWN_FACES_DIR, filename)

        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if encodings:
            known_encodings.append(encodings[0])
            known_names.append(name)
            print(f"[INFO] Encoded {name}")
        else:
            print(f"[WARNING] No face found in {filename}")

# Save encodings
with open(ENCODINGS_FILE, "wb") as f:
    pickle.dump((known_names, known_encodings), f)

print(f"[INFO] Saved {len(known_names)} encodings to {ENCODINGS_FILE}")
