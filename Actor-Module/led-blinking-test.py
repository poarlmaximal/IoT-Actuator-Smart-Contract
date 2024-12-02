from machine import Pin
import network
import time
from umqtt.simple import MQTTClient
import config  # Import the config file

# MQTT Callback Function
def on_message(topic, msg):
    message = msg.decode('utf-8')  # Decode the incoming message
    print(f"Message received: {message}")
    if message == f"{config.DEVICE_NAME} reset.":
        led.value(0)
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is reset.")
    elif message == f"{config.DEVICE_NAME} on.":
        led.value(1)
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is on.")
    elif message == f"{config.DEVICE_NAME} off.":
        led.value(0)
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is off.")

# LED Setup
led = Pin(config.PIN_LED, Pin.OUT)

# Wi-Fi Connection Function
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    
    attempt = 0
    while not wlan.isconnected() and attempt < 15:
        print("Connecting to Wi-Fi...")
        time.sleep(1)
        attempt += 1

    if wlan.isconnected():
        print("Connected to Wi-Fi:", wlan.ifconfig())
        return True
    else:
        print("Failed to connect to Wi-Fi.")
        return False

# MQTT Connection Function
def connect_mqtt():
    global client
    client = MQTTClient(config.DEVICE_NAME, config.MQTT_BROKER_IP_ADDRESS)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(b"iot/master")
    print("Connected to MQTT broker and subscribed to topic.")
    return client

# Main Function
def main():
    if not connect_wifi():
        return
    
    connect_mqtt()
    client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is ready.")
    
    loop_count = 0
    max_loops = 30  # Max loop iterations
    
    while loop_count < max_loops:
        client.check_msg()  # Check for incoming MQTT messages
        
        led.value(1)
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is on.")
        time.sleep(1)
        
        led.value(0)
        client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is off.")
        time.sleep(1)
        
        loop_count += 1
    
    client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} has stopped after {max_loops} cycles.")
    print("Program ended.")
    
if __name__ == "__main__":
    main()
