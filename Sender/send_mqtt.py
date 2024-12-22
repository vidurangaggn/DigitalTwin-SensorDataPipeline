import json
import paho.mqtt.client as mqtt
import time
import os

# MQTT settings
HONO_HOST = "your-hono-server-host"
HONO_PORT = 1883  # default MQTT port
HONO_USERNAME = "your-username"
HONO_PASSWORD = "your-password"
TENANT = "your-tenant"

# Device IDs for each floor
DEVICE_IDS = {
    "floor_1": "floor-1",
    "floor_2": "floor-2",
    "floor_3": "floor-3"
}

# Function to send data to Hono server
def send_to_hono(filename, topic):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        payload = json.dumps(data)
        result = client.publish(topic, payload)
        status = result[0]
        if status == 0:
            print(f"Successfully sent data from {filename} to topic {topic}")
        else:
            print(f"Failed to send data from {filename}")
    except Exception as e:
        print(f"Exception occurred while sending data from {filename}: {e}")

# Define MQTT callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Hono server")
    else:
        print(f"Failed to connect, return code {rc}\n")

def on_publish(client, userdata, mid):
    print("Data published")

def connect_to_hono(client, max_retries=50, retry_delay=5):
    for attempt in range(max_retries):
        try:
            client.connect(HONO_HOST, HONO_PORT, 60)
            client.loop_start()
            print("Attempting to connect to Hono server...")
            return True
        except Exception as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            time.sleep(retry_delay)
    return False

# Initialize MQTT client
client = mqtt.Client()
client.username_pw_set(HONO_USERNAME, HONO_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

# Try to connect to Hono server with retries
if not connect_to_hono(client):
    print("Failed to connect to Hono server after multiple attempts.")
    exit(1)

# List of JSON files and corresponding device topics
json_files_and_topics = {
    "floor_1": [
        'floor_1_voltage_data.json',
        'floor_1_current_data.json',
        'floor_1_power_meter_data.json',
        'floor_1_temp_data.json',
        'floor_1_smoke_detector_data.json'

    ],
    "floor_2": [
        'floor_2_voltage_data.json',
        'floor_2_current_data.json',
        'floor_2_power_meter_data.json',
        'floor_2_temp_data.json',
        'floor_2_smoke_detector_data.json'
    ],
    "floor_3": [
        'floor_3_voltage_data.json',
        'floor_3_current_data.json',
        'floor_3_power_meter_data.json',
        'floor_3_temp_data.json',
        'floor_3_smoke_detector_data.json'
    ]
}

# Send data for each floor
for floor, files in json_files_and_topics.items():
    device_id = DEVICE_IDS[floor]
    topic = f"telemetry/{TENANT}/{device_id}"
    
    for json_file in files:
        if os.path.exists(json_file):
            send_to_hono(json_file, topic)
            time.sleep(1)  # short delay between sends

client.loop_stop()
client.disconnect()
