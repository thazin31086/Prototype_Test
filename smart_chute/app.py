from flask import Flask, jsonify, render_template
import random
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Simulate static sensor data
    simulated_data = {
        "temperature": round(random.uniform(30.0, 40.0), 2),
        "pressure": round(random.uniform(100.0, 105.0), 2),
        "status": random.choice(["Safe", "Warning", "Danger"])
    }
    return jsonify(simulated_data)

if __name__ == '__main__':
    app.run(debug=True)
