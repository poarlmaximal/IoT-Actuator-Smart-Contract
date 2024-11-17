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

# Hauptfunktion
def main():
    connect_wifi()
    connect_mqtt()
    mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is ready.")

    while True:
        # Hier kannst du die LED-Steuerung implementieren
        # Beispiel: LED ein- und ausschalten
        # to do: Hier wahrscheinlich noch den Code von micropython.py reinpasten
        led.value(1)  # LED einschalten
        mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is on.")
        time.sleep(5)  # 5 Sekunden warten
        led.value(0)  # LED ausschalten
        mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is off.")
        time.sleep(5)  # 5 Sekunden warten

if __name__ == "__main__":
    main()
