import requests
import random
import time
from requests.exceptions import Timeout, RequestException

# --- Parameters ---
num_requests = 1000  # Total number of requests
timeout_seconds = 1  # Timeout for each request (seconds)
strategies = ["GET", "POST"]
endpoints = ["data-03", "data-04", "data-05"]

# --- Results Dictionary ---
results = {}

def make_request(strategy, endpoint, timeout):
    url = f"http://127.0.0.1:5000/{endpoint}"
    try:
        if strategy == "GET":
            response = requests.get(url, timeout=timeout)
        else:  # POST
            data = {"test_data": f"Hello {endpoint}!"}
            response = requests.post(url, json=data, timeout=timeout)

        if response.status_code == 444:  # Our custom packet loss code
            return "lost"
        elif response.status_code == 200:
            return "success"
        else:
            return "error"

    except Timeout:
        return "timeout"
    except RequestException:
        return "error"

# Test each endpoint with each strategy
for endpoint in endpoints:
    results[endpoint] = {}

    for strategy in strategies:
        successes = 0
        timeouts = 0
        packet_losses = 0
        errors = 0

        print(f"\nTesting {strategy} requests for {endpoint}...")
        start_time = time.time()

        for i in range(num_requests):
            result = make_request(strategy, endpoint, timeout_seconds)

            if result == "success":
                successes += 1
            elif result == "timeout":
                timeouts += 1
            elif result == "lost":
                packet_losses += 1
            else:
                errors += 1

            if (i + 1) % 100 == 0:
                print(f"Processed {i + 1} requests...")

        total_time = time.time() - start_time

        results[endpoint][strategy] = {
            "success_rate": successes / num_requests,
            "timeout_rate": timeouts / num_requests,
            "packet_loss_rate": packet_losses / num_requests,
            "error_rate": errors / num_requests,
            "total_time": total_time,
            "requests_per_second": num_requests / total_time
        }

# Print Results
print("\n=== Request Testing Results ===")
for endpoint in endpoints:
    print(f"\n--- Results for {endpoint} ---")
    for strategy, metrics in results[endpoint].items():
        print(f"\nStrategy: {strategy}")
        print(f"Success Rate: {metrics['success_rate']:.4f}")
        print(f"Timeout Rate: {metrics['timeout_rate']:.4f}")
        print(f"Packet Loss Rate: {metrics['packet_loss_rate']:.4f}")
        print(f"Error Rate: {metrics['error_rate']:.4f}")
        print(f"Total Time: {metrics['total_time']:.2f} seconds")
        print(f"Requests/second: {metrics['requests_per_second']:.2f}")
