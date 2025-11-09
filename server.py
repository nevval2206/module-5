from flask import Flask, request, jsonify
import random
import time

app = Flask(__name__)

# Set packet loss rates for different endpoints
PACKET_LOSS_RATES = {
    "data-03": 0.03,
    "data-04": 0.04,
    "data-05": 0.05
}

# Set timeout simulation rates (probability of slow response)
TIMEOUT_SIMULATION_RATES = {
    "data-03": 0.10,  # 10% chance of slow response
    "data-04": 0.15,  # 15% chance of slow response
    "data-05": 0.20   # 20% chance of slow response
}

@app.route('/data-03', methods=['GET', 'POST'])
@app.route('/data-04', methods=['GET', 'POST'])
@app.route('/data-05', methods=['GET', 'POST'])
def handle_data():
    # Get the endpoint from the request
    endpoint = request.path.lstrip('/')

    # Simulate timeout by adding random delay
    if random.random() < TIMEOUT_SIMULATION_RATES[endpoint]:
        # Random delay: either 0.6 seconds (exceeds 0.5s timeout) or instant (0s)
        delay = random.choice([0.6, 0.0])
        time.sleep(delay)

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
