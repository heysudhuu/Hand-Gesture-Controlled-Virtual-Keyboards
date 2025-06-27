# 🧠 Hand Gesture Controlled Virtual Keyboard

A Python-based **Virtual Keyboard** that lets you type using only hand gestures detected through your webcam! Built using **OpenCV**, **MediaPipe**, and **PyAutoGUI**, this project is a fun and practical demonstration of computer vision and gesture control.

---

## 📸 Demo

![Demo GIF](Demo.gif)  

---

## 🛠️ Technologies Used

- [Python](w)
- [OpenCV](w) – for video capture and image processing
- [MediaPipe](w) – for real-time hand tracking
- [PyAutoGUI](w) – to simulate actual keyboard inputs
- [Math](w), [NumPy](w) – for gesture distance calculations

---

## ✨ Features

- Virtual QWERTY keyboard layout rendered on screen  
- **Index finger hover** detects which key you're pointing at  
- **Tap gesture** (index + middle finger close) triggers key press  
- Real-time text rendering above the keyboard  
- Support for:
  - Letters (A–Z)
  - Space bar
  - Backspace

---

## 🧠 How It Works

1. Webcam captures live feed.
2. MediaPipe detects hand landmarks (index/middle fingertips).
3. Index finger position determines hovered key.
4. A "tap" gesture (fingers close) triggers typing that key.
5. `PyAutoGUI` simulates the actual key press on your system.

---

## 🚀 Getting Started

### Prerequisites

Install dependencies:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

*Run the Project*
```bash
python index.py
```

*📂 Project Structure*
```bash
.
├── index.py         # Main Python script
└── README.md        # Project documentation
```

📌 Notes
Works best in well-lit environments.

Designed for single-hand interaction (right or left).

The delay is managed to prevent accidental double-taps.

📄 License
MIT License © 2025 [Sudhanshu Yadav]
