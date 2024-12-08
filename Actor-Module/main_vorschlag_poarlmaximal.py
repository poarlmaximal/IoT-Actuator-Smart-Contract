# ------------- imports ----------------------

from machine import Pin
from machine import RTC
from network import WLAN
from time import sleep
from umqtt.simple import MQTTClient
import esp32
import config
import urequests
import ujson

# --------------- functions ------------------

# function for establishing wifi-connection
def connect_wifi():
    if not wlan.isconnected():
        print('connecting to wlan')
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
    topic_decoded = topic.decode('utf-8')
    msg_decoded = msg.decode('utf-8')
    print('Erhaltene Nachricht:', topic_decoded, msg_decoded)
    if msg_decoded == config.MQTT_MASTER_RESET_COMMAND:
        led.value(0)
        client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_RESET )

# establishing connection to MQTT Broker
def connect_mqtt():
    print('connecting to mqtt')
    client = MQTTClient(config.MQTT_CLIENT_NAME, config.MQTT_BROKER, config.MQTT_PORT)
    client.set_callback(on_message)
    try:
        client.connect()
        print("MQTT-Verbindung erfolgreich!")
    except Exception as e:
        print("MQTT-Verbindung nicht erfolgreich:",e)
    client.subscribe(config.MQTT_TOPIC_SUB)
    return client

# --------------- main ---------------------
# initialisiere Real-Time-Clock und LED-Pin
print("Hello World!")
rtc = RTC()
global led
led = Pin(13, Pin.OUT)

while True: 
    try: 
        # Verbindung zum Wi-Fi aufbauen
        wlan = WLAN()
        wlan.active(True)
        connect_wifi()
        
        # Verbindung zum MQTT-Server aufbauen und das Ready-Signal publishen
        global client
        client = connect_mqtt()
        client.publish(config.MQTT_TOPIC_PUB, config.MQTT_ACTOR_STATUS_READY)
        
        # LED entsprechend Blockchain LED-State ändern und Debugging-Ausgaben: Real-Time, ESP-Temperatur, LED-Status aus dem Sepolia-Netzwerk
        while wlan.isconnected():
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
                
            datetime = rtc.datetime()
            print(str(datetime[4])+":"+str(datetime[5])+":"+str(datetime[6])+"\t"+str(esp32.raw_temperature())+"°F"+"\t"+str(ledStatus)+'\t'+str(led.value()))
            sleep(10)
    except Exception as e: 
        print("Ein Fehler ist aufgetreten:", e)
        
