import numpy as np
import time
import json

# Smoke Detector Data Generation
def generate_smoke_detector_data(mean_smoke_level=0, std_dev_smoke=2):
    smoke_level = np.random.normal(mean_smoke_level, std_dev_smoke)
    smoke_level = max(smoke_level, 0)  # Smoke level cannot be negative
    alarm = 1 if smoke_level > 5 else 0  # Example threshold for alarm
    timestamp = time.time()
    return {
        "timestamp": timestamp,
        "smoke_level": smoke_level,
        "alarm": alarm
    }

if __name__ == "__main__":
    floor_files = {
        "floor_1": "floor_1_smoke_data.json",
        "floor_2": "floor_2_smoke_data.json",
        "floor_3": "floor_3_smoke_data.json"
    }

    while True:
        for floor, filename in floor_files.items():
            smoke_detector_data = generate_smoke_detector_data()

            print(f"{floor} data: {smoke_detector_data}")

            with open(filename, 'w') as f:
                json.dump(smoke_detector_data, f)
        
        time.sleep(5)  # Generate data every 5 seconds
