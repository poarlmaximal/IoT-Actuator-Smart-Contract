# main.py

from machine import Pin
import network
import time
import paho.mqtt.client as mqtt
import config  # Importiere die Konfigurationsdatei

# Callback-Funktion für eingehende MQTT-Nachrichten
def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Nachricht empfangen: {message}")
    # Check for reset command from the master module
    if message == f"{config.DEVICE_NAME} reset.":
        led.value(0)  # Turn off the LED
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is reset.")
    elif message == f"{config.DEVICE_NAME} on.":
        led.value(1)  # Turn on the LED
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is on.")
    elif message == f"{config.DEVICE_NAME} off.":
        led.value(0)  # Turn off the LED
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is off.")

# Setup für das LED-Pin
led = Pin(config.PIN_LED, Pin.OUT)  # Verwende den Pin aus der Konfiguration

# MQTT-Client initialisieren
mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message 

# Funktion zur WLAN-Verbindung
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)  # Station Interface
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    # Warte, bis die Verbindung hergestellt ist
    while not wlan.isconnected():
        print("Warten auf WLAN-Verbindung...")
        time.sleep(1)

    print("WLAN verbunden:", wlan.ifconfig())

# Verbinde zum MQTT-Broker und abonniere den Kanal
def connect_mqtt():
    mqtt_client.connect(config.MQTT_BROKER_IP_ADDRESS)
    mqtt_client.subscribe("iot/master")  # Abonniere den Master-Kanal
    mqtt_client.loop_start()  # Starte den MQTT-Loop

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

# Hauptfunktion
def main():
    connect_wifi()
    connect_mqtt()
    mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is ready.")
    
    # Zähler für die Durchläufe
    loop_count = 0
    max_loops = 30  # Maximale Anzahl an Schleifendurchläufen
    
    while loop_count < max_loops:
        led.value(1)  # LED einschalten
        mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is on.")
        time.sleep(1)  # 1 Sekunden warten
        
        led.value(0)  # LED ausschalten
        mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is off.")
        time.sleep(1)  # 1 Sekunden warten
        
        # Zähler erhöhen
        loop_count += 1
    
    # Nach 15 Durchläufen: Statusmeldung und Programmende
    mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} has stopped after {max_loops} cycles.")
    print("Programm beendet.")
    
if __name__ == "__main__":
    main()
