# :rocket: IoT Actuator Module with Smart Contract
## :pushpin: Project Description
This project is part of an IoT system for decentralized control of an actuator via a Smart Contract in an Ethereum test network. The actuator is controlled using an ESP32 module, which manages its state (on/off) through a Smart Contract. Communication is handled via MQTT for status exchange and Infura for blockchain interactions.

## 🏗️ System Architecture
The IoT system consists of the following main components:
- **Actuator Module (ESP32)** with LED control
- **Ethereum Smart Contract** for decentralized state management
- **MQTT Communication** for control and status updates
- **External Master Control** (not included in this repository) that interacts with the actuator module
### Communication Channels
- **MQTT:** The actuator module receives control commands on `iot/master` and sends status updates on `iot/Actor-1/status`.
- **Blockchain:** The actuator module queries the current LED state from the Smart Contract and can change it via a transaction.

## ⚙️ Setup & Installation
### Requirements
**Hardware:** 
- ESP32 DevKitC,
- LED
  
**Software:**
- MicroPython with Mu Editor
- MetaMask Wallet
- Infura API key for accessing the Ethereum test network (Sepolia)
- Mosquitto MQTT Broker (public or local)
### Installation
**1. Prepare ESP32:**
   - Install the required firmware (we used an older, stable version: esp32-20230426-v1.20.0.bin)
     
**2. Deploy the Smart Contract:**
   - Upload `led_contract.sol` to Remix IDE
   - Compile the Smart Contract with Solidity Compiler
   - Deploy the Smart Contract via MetaMask to the Ethereum test network Sepolia
   - Note the generated Smart Contract Address and Data (ABI for `readLed()`)
     
**3. Configure the Module:**
   - Enter your Wi-Fi credentials, Smart Contract address, Data and Infura API URL in config.py

## 🔧 Implementation
### Smart Contract (`led_contract.sol`)
- Contains the functions `setLed(int8 newOn)` and `readLed()`
- Allows switching the LED on/off and querying the current status

### Actuator Module (`main.py` and `config.py`)
**`main.py` handles:**
- Wi-Fi connection
- MQTT subscription and reaction to control commands
- Blockchain access for status verification and updates

**`config.py` stores key parameters:**
- Wi-Fi credentials
- MQTT broker and topics
- Smart Contract Information
- Infura API URL

## 🔌 MQTT Communication

| Topic              | Description                                        |
|--------------------|--------------------------------------------------|
| `iot/master`       | Receives control commands from the master module |
| `iot/Actor-1/status` | Sends status updates (ready, on, off, reset)   |


## 🧪 Testing & Debugging
### MQTT Tests
Use Mosquitto to test MQTT communication:

`mosquitto_sub -h broker.hivemq.com -t "iot/Actor-1/status" -V "mqttv311" -v`

`mosquitto_pub -h broker.hivemq.com -t "iot/master" -m "Master: Actor-1 reset." -V "mqttv311"`

### Blockchain Tests
- Transactions can be verified via Etherscan
- The current LED status can be queried using an eth_call request

## 📜 License 
- This project was developed as part of an IoT practicum
- License: MIT License
