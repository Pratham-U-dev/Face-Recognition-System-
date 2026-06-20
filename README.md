<div align="center">

# 🎭 Face Recognition System

**Real-time face detection & recognition powered by `dlib` and `OpenCV`**

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org)
[![face_recognition](https://img.shields.io/badge/face__recognition-1.3.0-FF6F61?style=flat-square)](https://github.com/ageitgey/face_recognition)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

A lightweight, two-script pipeline that encodes known faces from a photo directory and identifies them in real time through your webcam — no cloud APIs, no paid services, runs entirely offline.

![Demo Screenshot](face_recognition_project/Screenshot%20(14).png)

</div>

---

## ✨ Features

- 📸 **Batch face encoding** — scan an entire directory of photos and build a local face database in seconds
- 🎥 **Real-time webcam recognition** — live bounding-box overlay with name labels
- ⚡ **Frame-level performance optimisation** — frames are down-scaled 4× before inference, keeping CPU usage low
- 💾 **Persistent encodings** — serialised `.dat` file means you encode once and recognise forever
- 🔌 **Fully offline** — no API keys, no internet dependency, complete privacy

---

## 📁 Project Structure

```
face_recognition_project/
│
├── known_faces/               # 📂 Add your reference photos here (JPG/JPEG/PNG)
│   └── <person_name>.jpg      #    Filename (without extension) becomes the display label
│
├── encode_faces.py            # Step 1 — scan known_faces/ and build the encoding database
├── real_time_recognition.py   # Step 2 — live webcam recognition using the database
└── known_faces.dat            # Auto-generated — serialised face encodings (do not edit)
```

---

## 🚀 Quick Start

### 1 · Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.8 or higher |
| pip | latest |
| Webcam | any UVC-compatible device |
| CMake | required by `dlib` |

> **macOS / Linux:** `cmake` is usually available via `brew install cmake` or `sudo apt install cmake`.  
> **Windows:** Download the CMake installer from [cmake.org](https://cmake.org/download/).

### 2 · Clone the repository

```bash
git clone https://github.com/your-username/Face-Recognition-System.git
cd Face-Recognition-System/face_recognition_project
```

### 3 · Create a virtual environment *(recommended)*

```bash
python -m venv venv

# Activate — Linux / macOS
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate
```

### 4 · Install dependencies

```bash
pip install face_recognition opencv-python
```

> `face_recognition` automatically installs `dlib`, which compiles from source on first install. This may take a few minutes.

### 5 · Add your reference photos

Place one clear, front-facing photo per person inside the `known_faces/` directory.  
The **filename** (without extension) is used as the display label.

```
known_faces/
├── alice.jpg
├── bob.png
└── carol.jpeg
```

### 6 · Encode the faces

```bash
python encode_faces.py
```

Expected output:

```
[INFO] Encoding faces...
[INFO] Encoded alice
[INFO] Encoded bob
[INFO] Encoded carol
[INFO] Saved 3 encodings to known_faces.dat
```

### 7 · Run real-time recognition

```bash
python real_time_recognition.py
```

A window titled **"Face Recognition"** will open showing your webcam feed with live bounding boxes and name labels. Press **`q`** to quit.

---

## 🧠 How It Works

```
                  ┌─────────────────────────────────────────────┐
  ENCODING PHASE  │                                             │
                  │  known_faces/*.jpg  ──►  face_recognition   │
                  │                          .face_encodings()  │
                  │                               │             │
                  │                               ▼             │
                  │                       known_faces.dat       │
                  └─────────────────────────────────────────────┘

                  ┌─────────────────────────────────────────────┐
  INFERENCE PHASE │                                             │
                  │  Webcam Frame                               │
                  │      │                                      │
                  │      ▼                                      │
                  │  Resize 25%  ──►  Detect face locations     │
                  │                         │                   │
                  │                         ▼                   │
                  │                  Compute encodings          │
                  │                         │                   │
                  │                         ▼                   │
                  │              Compare vs known_faces.dat     │
                  │                         │                   │
                  │                         ▼                   │
                  │            Draw bounding box + label        │
                  └─────────────────────────────────────────────┘
```

| Script | Library | Method |
|---|---|---|
| `encode_faces.py` | `face_recognition` | `face_encodings()` — 128-d vector per face via dlib ResNet |
| `real_time_recognition.py` | `face_recognition` + `OpenCV` | `compare_faces()` — Euclidean distance threshold |

---

## ⚙️ Configuration

Both scripts expose a few constants at the top of the file that you can tweak without touching the logic:

**`encode_faces.py`**

```python
KNOWN_FACES_DIR = "known_faces"   # Path to your photo directory
ENCODINGS_FILE  = "known_faces.dat"  # Output file for the serialised database
```

**`real_time_recognition.py`**

```python
ENCODINGS_FILE = "known_faces.dat"  # Must match the encoder's output path
```

To adjust the **inference resolution trade-off**, change the scale factor inside the recognition loop:

```python
# Default — 25 % size (fast, less accurate on small faces)
small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

# Higher quality — 50 % size (slower, better on distant faces)
small_frame = cv2.resize(frame, (0, 0), fx=0.50, fy=0.50)
```

> Remember to update the corresponding scale-back multiplier (`*= 4` → `*= 2`) if you change `fx`/`fy`.

---

## 🐛 Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'face_recognition'` | Package not installed | `pip install face_recognition` |
| `dlib` compilation fails | Missing CMake or C++ toolchain | Install CMake + `build-essential` (Linux) or Xcode CLI tools (macOS) |
| `[WARNING] No face found in photo.jpg` | Photo is blurry or face is too small | Replace with a clear, front-facing, well-lit image |
| `[ERROR] Failed to grab frame from webcam` | Webcam not detected by OpenCV | Check `cv2.VideoCapture(0)` index — try `1` or `2` if you have multiple cameras |
| Recognition window doesn't open | No display / headless server | `real_time_recognition.py` requires a GUI. Use X11 forwarding on remote servers |
| Very low FPS | CPU bottleneck | Reduce `fx`/`fy` to `0.15`; or use GPU-accelerated dlib build |

---

## 🗺️ Roadmap

- [ ] `requirements.txt` and optional `Dockerfile`
- [ ] CLI argument support (`--source`, `--scale`, `--threshold`)
- [ ] Confidence score overlay on bounding boxes
- [ ] Multi-face tolerance tuning via `face_distance`
- [ ] Support for video file input in addition to webcam
- [ ] GPU acceleration path via CUDA dlib build
- [ ] Attendance logging to CSV

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. **Fork** the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a **Pull Request**

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [Adam Geitgey's `face_recognition`](https://github.com/ageitgey/face_recognition) — the backbone of this project
- [dlib](http://dlib.net/) by Davis King — the underlying deep-learning model
- [OpenCV](https://opencv.org/) — computer vision and webcam I/O

---

<div align="center">

Made with ❤️ · Give it a ⭐ if it helped you!

</div>
