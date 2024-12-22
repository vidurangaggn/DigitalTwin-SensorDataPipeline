import math
import numpy as np
import time
import json
import threading

# Function to generate a time-varying resistance value
def generate_resistance(mean_R=5, std_dev_R=1):
    return np.random.normal(mean_R, std_dev_R)

# Function to generate a time-varying reactance value
def generate_reactance(mean_X=20, std_dev_X=5):
    return np.random.normal(mean_X, std_dev_X)

# Voltage Sensor Data Generation influenced by resistance
def generate_voltage_data(t):
    # Generate random frequency between 50 and 60 Hz
    frequency = np.random.uniform(50, 60)

    # Calculate angular frequency
    omega = 2 * np.pi * frequency
    
    # Generate the voltage as a function of time
    voltage = 325.3 * np.sin(omega * t)

    # Add some noise to the voltage
    voltage += np.random.normal(0, 0.01 * abs(voltage))  # Adding some noise

    return voltage

# Current Sensor Data Generation influenced by resistance and reactance
def generate_current_data(voltage, R, X):
    impedance = complex(R, X)
    current = voltage / impedance  # Ohm's Law: V = IR => I = V/R
    current = np.abs(current)  # Current is a complex number, we only need the magnitude
    current += np.random.normal(0, 0.01 * abs(current))  # Adding some noise
    return current

# Power Meter Data Generation influenced by voltage and current
def generate_power_meter_data(voltage, current):
    active_power = voltage * current  # P = VI
    reactive_power = active_power * 0.5  # Example value, not realistic
    apparent_power = np.sqrt(active_power**2 + reactive_power**2)  # S = sqrt(P^2 + Q^2)
    return active_power, reactive_power, apparent_power

# Collect samples over one period
def collect_samples(duration, sampling_rate, mean_R, mean_X):
    samples = int(duration * sampling_rate)
    voltage_samples = []
    current_samples = []
    
    start_time = time.time()
    for _ in range(samples):
        t = time.time() - start_time
        
        # Generate time-varying resistance and reactance values
        R = generate_resistance(mean_R)
        X = generate_reactance(mean_X)
        
        # Generate sensor data influenced by resistance and reactance
        voltage = generate_voltage_data(t)
        current = generate_current_data(voltage, R, X)
        
        voltage_samples.append(voltage)
        current_samples.append(current)
        
        time.sleep(1 / sampling_rate)
    
    return voltage_samples, current_samples

# Calculate RMS value
def calculate_rms(values):
    squared_values = [v ** 2 for v in values]
    mean_squared_value = np.mean(squared_values)
    rms_value = math.sqrt(mean_squared_value)
    return rms_value

# Function to simulate sensor data collection for a floor
def simulate_floor(floor, mean_R, mean_X, sampling_rate, duration):
    while True:
        timestamp = time.time()
        
        # Collect voltage and current samples over one period
        voltage_samples, current_samples = collect_samples(duration, sampling_rate, mean_R, mean_X)
        
        # Calculate RMS values
        voltage_rms = calculate_rms(voltage_samples)
        current_rms = calculate_rms(current_samples)
        
        # Calculate active, reactive, and apparent power
        active_power, reactive_power, apparent_power = generate_power_meter_data(voltage_rms, current_rms)

        # Print the generated data
        print(f"Floor {floor} - Voltage RMS: {voltage_rms:.2f} V")
        print(f"Floor {floor} - Current RMS: {current_rms:.2f} A")
        print(f"Floor {floor} - Power Meter Data: Active Power: {active_power:.2f} W, Reactive Power: {reactive_power:.2f} VAR, Apparent Power: {apparent_power:.2f} VA")
    
        # Prepare data payloads
        power_data = {
            "timestamp": timestamp,
            "voltage_rms": voltage_rms,
            "current_rms": current_rms,
            "active_power": active_power,
            "apparent_power": apparent_power,
            "resistance": mean_R,
            "reactance": mean_X
        }
        
        # Save data to files
        with open(f'floor_{floor}_power_data.json', 'w') as f:
            json.dump(power_data, f)
        
        time.sleep(2)  # Generate data every 2 seconds

if __name__ == "__main__":
    mean_R = 5  # Mean resistance value
    mean_X = 20  # Mean reactance value
    sampling_rate = 500  # Samples per second
    duration = 1  # Duration to collect samples in seconds
    
    # Create threads for each floor
    floors = [
    {"floorNum": 1, "mean_R": 5, "mean_X": 20, "sampling_rate": 500, "duration": 1}, 
    {"floorNum": 2, "mean_R": 5, "mean_X": 20, "sampling_rate": 500, "duration": 1},
    {"floorNum": 3, "mean_R": 5, "mean_X": 20, "sampling_rate": 500, "duration": 1}
    ]

    threads = []
    for floor in floors:
        thread = threading.Thread(target=simulate_floor, args=(floor["floorNum"], floor["mean_R"], floor["mean_X"], floor["sampling_rate"], floor["duration"]))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
