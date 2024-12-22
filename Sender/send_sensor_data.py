import json
import requests
import time
import os
import publisher
from pika.exchange_type import ExchangeType


# Device IDs for each floor
DEVICE_IDS = {
    "floor_1": "floor1",
    "floor_2": "floor2",
    "floor_3": "floor3"
}

# Function to send data to Hono server via HTTP
def send_to_hono(filename, device_id):

    message_sender = publisher.getMessageSender()
    #Declare an exchnage
    exchange_name = "deviceDataExchange"
    message_sender.declare_exchange(exchange_name= exchange_name, exchange_type=ExchangeType.topic)

    data_type = ""

    if 'power' in filename:
        data_type = "power"
    elif 'temp' in filename:
        data_type = "temperature"
    elif 'smoke' in filename:
        data_type = "smoke"

    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        payload = json.dumps(data)

        message_sender.send_message(exchange=exchange_name, routing_key=f"{device_id}.{data_type}", body=payload)

        message_sender.close()

        print(f"Successfully sent data from {filename} to topic {device_id}.{data_type}")
    
    except Exception as e:
         print(f"Exception occurred while sending data from {filename}: {e}")

# Base64 encoding function for basic auth
import base64

# List of JSON files and corresponding device IDs
json_files_and_topics = {
    "floor_1": [
        'floor_1_power_data.json',
        'floor_1_temp_data.json',
        'floor_1_smoke_data.json'
    ],
    "floor_2": [
        'floor_2_power_data.json',
        'floor_2_temp_data.json',
        'floor_2_smoke_data.json'
    ],
    "floor_3": [
        'floor_3_power_data.json',
        'floor_3_temp_data.json',
        'floor_3_smoke_data.json'
    ]
}

# Send data for each floor
while True:
    for floor, files in json_files_and_topics.items():
        device_id = DEVICE_IDS[floor]
        for json_file in files:
            if os.path.exists(json_file):
                
                send_to_hono(json_file, device_id)
                time.sleep(1)  # short delay between sends