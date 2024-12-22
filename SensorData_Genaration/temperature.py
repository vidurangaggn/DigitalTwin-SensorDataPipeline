import numpy as np
import time
import json

# Data Generation for Temperature and Humidity
def generate_sensor_data(mean_temp=25, std_dev_temp=5, mean_humidity=50, std_dev_humidity=10):
    temperature = np.random.normal(mean_temp, std_dev_temp)
    humidity = np.random.normal(mean_humidity, std_dev_humidity)
    timestamp = time.time()
    return {
        "timestamp": timestamp,
        "temperature": temperature,
        "humidity": humidity
    }

if __name__ == "__main__":
    floor_files = {
        "floor_1": "floor_1_temp_data.json",
        "floor_2": "floor_2_temp_data.json",
        "floor_3": "floor_3_temp_data.json"
    }

    while True:
        for floor, filename in floor_files.items():
            sensor_data = generate_sensor_data()

            print(f"{floor} data: {sensor_data}")

            with open(filename, 'w') as f:
                json.dump(sensor_data, f)
        
        time.sleep(5)  # Generate data every 5 seconds
