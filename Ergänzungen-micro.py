# Import necessary modules
import network
import time
import urequests
import json
from machine import Pin

# Wi-Fi credentials
SSID = 'your_wifi_ssid'  # Change this to your Wi-Fi SSID
PASSWORD = 'your_wifi_password'  # Change this to your Wi-Fi password

# Smart contract details
CONTRACT_ADDRESS = 'your_contract_address'  # Change this to your smart contract address
ABI = '[{"constant":true,"inputs":[],"name":"readLed","outputs":[{"name":"","type":"int8"}],"payable":false,"stateMutability":"view","type":"function"}]'
FUNCTION_SIGNATURE = 'your_function_signature_here'  # Replace with the actual function signature
RPC_ENDPOINT = 'https://your_rpc_endpoint_address'  # Change to your JSON-RPC endpoint

# Initialize the LED pin
led = Pin(13, Pin.OUT)  # Change this pin number if needed
led.value(0)  # Turn LED off initially

# Function to connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Create a WLAN object in station mode
    wlan.active(True)  # Activate the WLAN interface
    wlan.connect(SSID, PASSWORD)  # Connect to the Wi-Fi network
    
    # Wait for the connection to establish
    attempt = 0
    while not wlan.isconnected() and attempt < 15:
        print("Connecting to Wi-Fi...")
        time.sleep(1)
        attempt += 1

    if wlan.isconnected():
        print("Connected to Wi-Fi:", wlan.ifconfig())  # Print the IP address and other info
        return True
    else:
        print("Failed to connect to Wi-Fi.")
        return False

# Function to read the LED state from the smart contract
def read_led_state():
    headers = {'Content-Type': 'application/json'}

    # JSON-RPC payload to call readLed function
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{
            "to": CONTRACT_ADDRESS,
            "data": '0x' + FUNCTION_SIGNATURE
        }, "latest"],
        "id": 1
    }

    try:
        # Send the request to the Ethereum node
        response = urequests.post(RPC_ENDPOINT, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            led_state = int(result.get('result', '0x0'), 16)  # Convert hex result to int
            response.close()  # Ensure response is closed
            return led_state
        else:
            print(f"Error reading LED state: {response.status_code} {response.text}")
            response.close()
            return None
    except Exception as e:
        print(f"Exception occurred while reading LED state: {e}")
        return None

# Function to toggle the LED based on the state
def toggle_led(state):
    if state == 1:
        led.value(1)  # Turn the LED on
    elif state == 0:
        led.value(0)  # Turn the LED off

# Main loop
def main():
    if not connect_wifi():  # Connect to Wi-Fi
        print("Wi-Fi connection failed. Exiting...")
        return

    print("Starting main loop...")
    while True:
        try:
            led_state = read_led_state()  # Read the LED state from the smart contract
            if led_state is not None:
                toggle_led(led_state)  # Toggle the LED based on the state
            else:
                print("No valid LED state received.")
        except Exception as e:
            print(f"Error in main loop: {e}")
        
        time.sleep(5)  # Wait for 5 seconds before the next check

# Run the main function
if __name__ == "__main__":
    main()
