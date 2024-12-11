# main.py

# ------------------ imports ------------------
from machine import Pin, RTC, reset
from network import WLAN
from time import sleep
from umqtt.simple import MQTTClient
import esp32
import config
import urequests
import ujson

# -------- declare and initialize global variables --------
led = Pin(13, Pin.OUT)
wlan = WLAN()
client = None

# --------------- functions -------------------
# function for establishing wifi-connection
def connect_wifi():
    global wlan
    if not wlan.isconnected():
        print('Connecting to WLAN...')
        wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("wlan.isconnected(): "+str(wlan.isconnected())+str(wlan.ifconfig()))

# function for reading ledStatus from blockchain (smart contract)
def read_led_status():
    led_status = 0
    json_data = {'jsonrpc':'2.0','method':'eth_call','params':[{'to':config.CONTRACT_ADDRESS,'data': config.DATA},'latest'],'id':1}
    json_payload = ujson.dumps(json_data)
    headers = {'Content-Type':'application/json'}
    try:
        response = urequests.post(config.RPC_URL, data=json_payload, headers=headers)
        result = response.json().get('result')
        led_status = int(result,16)
    except Exception as e:
        print("Error accessing the smart contract: ", e)
    return led_status

# function for reactions on messages
def on_message(topic, msg):
    global led
    global client
    # decode topic and message
    topic_decoded = topic.decode('utf-8')
    msg_decoded = msg.decode('utf-8')
    print('Received message:', topic_decoded, msg_decoded)
    if msg_decoded == config.MQTT_MASTER_RESET_COMMAND:
        led.value(0)
        client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_RESET, qos=1)
        reset()
        

# function for establishing the connection between MQTT-Client and MQTT-Broker
def connect_mqtt():
    global client
    print('Connecting to MQTT...')
    client = MQTTClient(config.MQTT_CLIENT_NAME, config.MQTT_BROKER, config.MQTT_PORT)
    client.set_callback(on_message)
    try:
        client.connect()
        print("MQTT connection initiated ...")
        while not client:
            pass
        print("MQTT connection successful!")
        client.subscribe(config.MQTT_TOPIC_SUB)
    except Exception as e:
        print("MQTT connection unsuccessful:",e)
    

# --------------- main ---------------------
# initialize Real-Time Clock
rtc = RTC()

# Introduce a helper variable led_value = -1, 
# so that on the very first run the state is published to the broker 
# (regardless of the ledStatus from the Smart Contract)
led_value = -1 

while True:
    try:
        # Establish connection to Wi-Fi
        wlan.active(True)
        connect_wifi()
        
        # Establish connection to the MQTT server and publish the Ready signal
        connect_mqtt()
        client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_READY)
        
        # Change LED according to the Blockchain LED-State and debugging outputs: Real-Time, ESP temperature, LED status from the Sepolia network.
        while wlan.isconnected():
            
            # respond to RESET message from the MQTT_BROKER
            client.check_msg()
            
            # read the ledStatus from the Smart Contract
            led_status = read_led_status()
            
            # respond to led_status changes
            if led_status != led_value:
                if led_status == 0:
                    led.value(0)
                    led_value = 0
                    client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_OFF)
                elif led_status == 1:
                    led.value(1)
                    led_value = 1
                    client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_ON)
                else:
                    print('Something went wrong...')
            
            datetime = rtc.datetime()
            print(str(datetime[4])+":"+str(datetime[5])+":"+str(datetime[6])+"\t"+str(esp32.raw_temperature())+"°F"+"\t"+str(led_status)+'\t'+str(led.value()))
            sleep(5)
    except Exception as e:
        print("An error has occurred:", e)
