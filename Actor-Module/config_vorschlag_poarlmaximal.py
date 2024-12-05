# config.py

# Device Name of the actor module
DEVICE_NAME = 'Actor-1'

# Pin number for the LED
PIN_LED = 13

# Wi-Fi
WIFI_SSID = '...'
WIFI_PASSWORD = '...'

# MQTT
MQTT_BROKER = 'test.mosquitto.org'
MQTT_SERVER_TCP_PORT = 1883
MQTT_CLIENT_NAME = 'Actor-1'
MQTT_TOPIC_SUB = 'iot/master'
MQTT_TOPIC_PUB = 'iot/Actor-1/status'
MQTT_MASTER_RESET_COMMAND = 'Master: Actor-1 reset.'
MQTT_ACTOR_STATUS_READY = 'Actor-1 is ready'
MQTT_ACTOR_STATUS_RESET = 'Actor-1 is reset.'
MQTT_ACTOR_STATUS_ON = 'Actor-1 is on.'
MQTT_ACTOR_STATUS_OFF = 'Actor-1 is off.'


# MetaMask
WALLET_ADDRESS = '...'
WALLET_PRIVATE_KEY = '...'
CONTRACT_ADDRESS = '0x3fDF2202E69EeDBdaB9c714625BB27bf593A4429'
DATA = '0xa5480959'

# Infura
RPC_URL = '...'
