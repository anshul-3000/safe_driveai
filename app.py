from flask import Flask, Response, jsonify
from drowsiness import DrowsinessDetector
import threading
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
app.secret_key = "your_secret_key"

detector = DrowsinessDetector()

@app.route('/')
def home():
    return jsonify({"message": "Drowsiness Detection API is running."}), 200

@app.route('/calibrate')
def calibrate():
    detector.mode = 'calibration'
    threading.Thread(target=detector.calibrate).start()
    return jsonify({"message": "Calibration started."}), 200

@app.route('/monitor')
def monitor():
    if not detector.calibration_complete:
        return jsonify({"error": "Please calibrate first."}), 400
    detector.mode = 'monitor'
    threading.Thread(target=detector.monitor).start()
    return jsonify({"message": "Monitoring started."}), 200

@app.route('/stop')
def stop():
    detector.stop()
    return jsonify({"message": "Monitoring stopped."}), 200

@app.route('/reset')
def reset():
    print("System reset requested")
    return jsonify({"message": "System reset."}), 200

@app.route('/video_feed')
def video_feed():
    return Response(detector.generate_video(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
