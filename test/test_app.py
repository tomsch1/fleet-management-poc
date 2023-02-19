import logging
import random
import requests
import sys


# Configure logging
logging.basicConfig(filename='test.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Define the base URL of the API
base_url = f"http://{sys.argv[1]}:5000"

# Define the list of device IDs
device_ids = [112, 358, 132, 134]

# Retrieve a random device ID
device_id = random.choice(device_ids)
logging.info(f"Retrieved random device ID {device_id}")

# Check if the device is already present in the database
response = requests.get(f"{base_url}/devices/{device_id}")
if response.status_code == 200:
    # Device is already present, delete it
    response = requests.delete(f"{base_url}/devices/{device_id}")
    response.raise_for_status()
    logging.info(f"Deleted device with ID {device_id}")
else:
    # Device is not present, add it
    device = {
        'name': f"Device{device_id}",
        'type': 'Coffee',
        'location': 'Entrance'
    }
    response = requests.post(f"{base_url}/devices/{device_id}", json=device)
    response.raise_for_status()
    logging.info(f"Added device '{device['name']}' with ID {response.json()['id']}")

    # Modify the properties of the device
    device['name'] = f"Device_{device_id}"
    device['type'] = 'Fridge'
    device['location'] = 'Office'
    response = requests.put(f"{base_url}/devices/{response.json()['id']}", json=device)
    response.raise_for_status()
    logging.info(f"Updated device with ID {response.json()['id']}")
