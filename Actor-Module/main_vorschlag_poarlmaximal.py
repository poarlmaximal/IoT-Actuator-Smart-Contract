# ------------- imports ----------------------

from machine import Pin
from machine import RTC
from network import WLAN
from time import sleep, time
from umqtt.simple import MQTTClient
import esp32
import config
import urequests
import ujson
reset_pending = False
client = None

# --------------- functions ------------------

# function for establishing wifi-connection
def connect_wifi():
    if not wlan.isconnected():
        print('Lost Wi-Fi connection. Reconnecting...')
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("wlan.isconnected(): "+str(wlan.isconnected())+str(wlan.ifconfig()))

# function for reading LED state out of blockchain
def readLedStatus():
    ledStatus = 0
    json_data = {'jsonrpc':'2.0','method':'eth_call','params':[{'to':config.CONTRACT_ADDRESS,'data': config.DATA},'latest'],'id':1}
    json_payload = ujson.dumps(json_data)
    headers = {'Content-Type':'application/json'}
    try:
        response = urequests.post(config.RPC_URL, data=json_payload, headers=headers)
        print(response)
        print(type(response))
        print(response.json())
        result = response.json().get('result')
        print(result)
        print(type(result))
        ledStatus = int(result,16)
    except Exception as e:
        print("Fehler beim Zugriff auf den Smart Contract: ", e)
    return ledStatus

# reactions on messages
def on_message(topic, msg):
    # topic und message decodieren
    global reset_pending
    topic_decoded = topic.decode('utf-8')
    msg_decoded = msg.decode('utf-8')
    print(f"Received MQTT Message: Topic={topic_decoded}, Message={msg_decoded}")
    if msg_decoded == config.MQTT_MASTER_RESET_COMMAND:
        print("Reset command received.")
        reset_pending = True  # Set flag to handle publish in the main loop
    else:
        print(f"Unrecognized MQTT command: {msg_decoded}")
 
# establishing connection to MQTT Broker
def connect_mqtt():
    global client
    print('connecting to mqtt')
    client = MQTTClient(
        config.MQTT_CLIENT_NAME,
        config.MQTT_BROKER,
        config.MQTT_PORT,
        keepalive=60
    )
    # Setting Last-Will Message
    client.set_last_will(
        config.MQTT_TOPIC_PUB,
        "Device disconnected unexpectedly",
        retain=False,
        qos=1
    )
    client.set_callback(on_message)
    try:
        client.connect()
        print("MQTT-Verbindung erfolgreich!")
        if client:
            client.subscribe(config.MQTT_TOPIC_SUB)
            print(f"Subscribed to topic: {config.MQTT_TOPIC_SUB}")
    except Exception as e:
        print("MQTT-Verbindung nicht erfolgreich:", e)
        client = None
    return client

# --------------- main ---------------------
# initialisiere Real-Time-Clock und LED-Pin
print("Hello World!")
rtc = RTC()
led = Pin(13, Pin.OUT)

# Verbindung zum Wi-Fi aufbauen
wlan = WLAN()
wlan.active(True)

while True:
    try:
        connect_wifi()
        # Verbindung zum MQTT-Server aufbauen und das Ready-Signal publishen
        mqtt_reconnect_start = time()
        if client is None:
            print("Lost MQTT connection. Reconnecting...")
            client = connect_mqtt()
            mqtt_reconnect_end = time()
            reconnect_duration = mqtt_reconnect_end - mqtt_reconnect_start
            if client is not None:
                client.publish(
                    config.MQTT_TOPIC_PUB, 
                    f"Connection re-established after a timeout of {reconnect_duration:.2f} seconds"
                )
                print(f"Connection re-established after {reconnect_duration:.2f} seconds.")
            else:
                print("MQTT client is not initialized.")
        if client:
            client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_READY)
        
        # LED entsprechend Blockchain LED-State ändern und Debugging-Ausgaben: Real-Time, ESP-Temperatur, LED-Status aus dem Sepolia-Netzwerk
        while wlan.isconnected():
            client.check_msg()  # Non-blocking message handling
            ledStatus = readLedStatus()

            if ledStatus != led.value():
                if ledStatus == 0:
                    led.value(0)
                    client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_OFF)
                elif ledStatus == 1:
                    led.value(1)
                    client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_ON)
                else:
                    print('irgendwas ist schief gegangen')
                    
            if reset_pending and client:
                try:
                    print("Performing reset actions...")
                    led.value(0)  # Reset LED state to OFF
                    client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_RESET)
                    print("Reset status published successfully.")
                    reset_pending = False  # Clear the flag after successful publish
                    sleep(5)  # Sleep for 5 seconds after handling reset
                except Exception as e:
                    print("Error during reset publish:", e)
                    print("Lost MQTT connection. Reconnecting...")
                    mqtt_reconnect_start = time()
                    client = connect_mqtt()
                    mqtt_reconnect_end = time()
                    reconnect_duration = mqtt_reconnect_end - mqtt_reconnect_start
                    if client is not None:
                        client.publish(
                            config.MQTT_TOPIC_PUB, 
                            f"Connection re-established after a timeout of {reconnect_duration:.2f} seconds"
                        )
                        print(f"Connection re-established after {reconnect_duration:.2f} seconds.")

            datetime = rtc.datetime()
            fahrenheit_temp = esp32.raw_temperature()
            celsius_temp = (fahrenheit_temp - 32) * 5 / 9
            print(
                str(datetime[4])
                + ":"
                + str(datetime[5])
                + ":"
                + str(datetime[6])
                + "\t"
                + "{:.2f}°C".format(celsius_temp)  # Display Celsius temperature
                + "\t"
                + str(ledStatus)
                + "\t"
                + str(led.value())
            )
            sleep(1)  # Sleep for a shorter duration to ensure responsiveness
    except Exception as e:
        print("Ein Fehler ist aufgetreten:", e)
        sleep(5)
