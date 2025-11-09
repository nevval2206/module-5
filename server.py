from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Set packet loss rates for different endpoints
PACKET_LOSS_RATES = {
    "data-03": 0.03,
    "data-04": 0.04,
    "data-05": 0.05
}

@app.route('/data-03', methods=['GET', 'POST'])
@app.route('/data-04', methods=['GET', 'POST'])
@app.route('/data-05', methods=['GET', 'POST'])
def handle_data():
    # Get the endpoint from the request
    endpoint = request.path.lstrip('/')

    # Simulate packet loss based on the endpoint
    if random.random() < PACKET_LOSS_RATES[endpoint]:
        return '', 444  # Custom status code for simulated packet loss

    if request.method == 'GET':
        return jsonify({
            "message": f"Data retrieved successfully from {endpoint}",
            "status": "success"
        })

    elif request.method == 'POST':
        data = request.get_json()
        return jsonify({
            "message": f"Data received successfully at {endpoint}",
            "received_data": data,
            "status": "success"
        })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
