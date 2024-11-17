# IoT-Actuator-Smart-Contract
This project is part of an internship in the Internet of Things (IoT) module and develops a simple IoT system for decentralized control of an actuator (LED), which is switched via a smart contract in an Ethereum test network.

## Project Overview
The goal of the project is to implement an IoT system consisting of the following components:

1. **Smart Contract (completed)**: A Solidity smart contract controls the state of an actuator (LED), which is controlled by an ESP32 microcontroller module.
2. **Actuator Module (in development)**: An ESP32-DevKitC that controls the LED and interacts with the smart contract.
3. **Sensor Module (in development)**: An ESP32-based sensor module that collects environmental data and publishes it via MQTT.
4. **Communication Interfaces**: MQTT and BLE for communication between modules and control via a smartphone app.

## Installation und Einrichtung

### Voraussetzungen

- **MetaMask**: Installiere die [MetaMask-Erweiterung](https://metamask.io/) für den Browser, um mit dem Ethereum-Testnetzwerk zu interagieren.
- **Remix IDE**: Nutze die webbasierte Entwicklungsumgebung [Remix](https://remix.ethereum.org/) für den Smart Contract.
- **MQTT-Client und Mosquitto**: Für die MQTT-Kommunikation wird der Mosquitto-Client verwendet (siehe [Mosquitto Download](https://mosquitto.org/download/)).


------------------------
## Aktueller Stand
Der Smart Contract ist fertiggestellt und implementiert die grundlegenden Funktionen zur Steuerung des Aktors: 

- **setLed(int8 newOn)**: Setzt den Zustand der LED. newOn = 1 schaltet die LED ein, newOn = 0 schaltet sie aus.
- **readLed()**: Gibt den aktuellen Zustand der LED zurück.
- **retrieveEther()**: Ermöglicht dem Besitzer des Contracts, Ether abzuheben.
- **kill()**: Entfernt den Contract aus der Blockchain.

Der Contract ist für das Sepolia Testnetzwerk vorbereitet und wird in der Entwicklungsumgebung [Remix](https://remix.ethereum.org/) getestet. Eine detaillierte Anleitung zur Verwendung und Testung findet sich in [todo/doing]. 


## Todo: 
bis 20.11. 16:00 - 18:00 Uhr
- Readme aktualisieren
- micropython.py verstehen und je nach chain eintrag die LED setzen und die Aktualisierung über MQTT publishen (idealerweise fügen wir das dann noch sinnvoll ins main ein)
