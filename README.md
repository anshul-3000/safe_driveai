# 🛡️ SafeDrive AI - Backend

The backend of **SafeDrive AI** – an intelligent real-time drowsiness detection system powered by Flask, OpenCV, and Pygame. It monitors facial cues through your webcam, detects signs of drowsiness, and triggers an alarm for driver safety. This backend is designed to work seamlessly with a React + Bootstrap-based frontend.

> ⚠️ **Note:** This backend is intended to be run **locally** so that the alarm (sound) feature works properly. Most cloud platforms (like Render, Railway) do not support server-side audio playback.

---

## 🚀 Features

- 🧠 Real-time drowsiness detection using OpenCV
- 👁️ Eye and face detection with Haar cascades
- 🔊 Alarm alert using Pygame when drowsiness is detected
- 🎥 Live video feed via MJPEG stream
- 📡 Flask RESTful endpoints for full frontend integration
- 💻 Compatible with React frontend (see link below)

---

# 🔗 Live Frontend Demo

👉 [Live Demo](https://rad-centaur-e5c343.netlify.app/)  
(Backend must be running locally for full functionality, including the alarm)

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/anshul-3000/safe_driveai.git
cd safe_driveai/backend
```

### 2. Install Dependencies
Make sure Python 3.8+ is installed.
```bash
pip install -r requirements.txt
```

### 3. Run the Flask Server
For local development:
```bash
python app.py
```

For production:
```bash
gunicorn app:app --bind 0.0.0.0:5000
```

### 4. API Endpoints
- Endpoint	Method	Description
- /calibrate	GET	Starts calibration process
- /monitor	GET	Begins real-time drowsiness monitoring
- /stop	GET	Stops current operation
- /reset	GET	Resets state
- /video_feed	GET	Returns MJPEG video feed
  
### 📁 Project Structure
```php
backend/
├── app.py              # Flask app with routes
├── detector.py         # DrowsinessDetector class
├── static/
│   └── music.wav       # Alarm sound file
├── requirements.txt    # Python dependencies
└── README.md           # You are here
```

### 🔗 Frontend Repository
Check out the professional React frontend here:
- [👉 SafeDrive AI Frontend Repo](https://github.com/anshul-3000/safe_driveai_frontend)
- 🧠 Tech Stack
      - Python 3
      - Flask
      - OpenCV
      - Pygame
      - Haar Cascades
      - Gunicorn (for production)

### 🙌 Author
Anshul Chaudhary
- Machine Learning Engineer | Full-Stack Developer
- 🚀 Passionate about AI, ML, NLP & real-time applications
