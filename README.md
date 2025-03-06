# IoT Actuator Module with Smart Contract
## Project Description
This project is part of an IoT system for decentralized control of an actuator via a Smart Contract in an Ethereum test network. The actuator is controlled using an ESP32 module, which manages its state (on/off) through a Smart Contract. Communication is handled via MQTT for status exchange and Infura for blockchain interactions.

## System Architecture
The IoT system consists of the following main components:
- **Actuator Module (ESP32)** with LED control
- **Ethereum Smart Contract** for decentralized state management
- **MQTT Communication** for control and status updates
- **External Master Control** (not included in this repository) that interacts with the actuator module
### Communication Channels
- **MQTT:** The actuator module receives control commands on 'iot/master' and sends status updates on 'iot/Actor-1/status'.
- **Blockchain:** The actuator module queries the current LED state from the Smart Contract and can change it via a transaction.

## Setup & Installation
### Requirements
Hardware: 
- ESP32 DevKitC,
- LED
  
Software:
- MicroPython with Mu Editor
- MetaMask Wallet
- Infura API key for accessing the Ethereum test network (Sepolia)
- Mosquitto MQTT Broker (public or local)
### Installation
1. Prepare ESP32
   - Install the required firmware (we used an older, stable version: esp32-20230426-v1.20.0.bin)
2. Deploy the Smart Contract
   - Upload led_contract.sol to Remix IDE
   - Compile the Smart Contract with Solidity Compiler
   - Deploy the Smart Contract via MetaMask to the Ethereum test network Sepolia
   - Note the generated Smart Contract Address and Data (ABI for readLed())
3. Configure the Module
   - Enter your Wi-Fi credentials, Smart Contract address, Data and Infura API URL in config.py



### Voraussetzungen

- **MetaMask**: Installiere die [MetaMask-Erweiterung](https://metamask.io/) für den Browser, um mit dem Ethereum-Testnetzwerk zu interagieren.
- **Remix IDE**: Nutze die webbasierte Entwicklungsumgebung [Remix](https://remix.ethereum.org/) für den Smart Contract.
- **MQTT-Client und Mosquitto**: Für die MQTT-Kommunikation wird der Mosquitto-Client verwendet (siehe [Mosquitto Download](https://mosquitto.org/download/)).


------------------------
## Aktueller Stand des Smart Contracts
Der Smart Contract ist fertiggestellt und implementiert die grundlegenden Funktionen zur Steuerung des Aktors: 

- **setLed(int8 newOn)**: Setzt den Zustand der LED. newOn = 1 schaltet die LED ein, newOn = 0 schaltet sie aus.
- **readLed()**: Gibt den aktuellen Zustand der LED zurück.
- **retrieveEther()**: Ermöglicht dem Besitzer des Contracts, Ether abzuheben.
- **kill()**: Entfernt den Contract aus der Blockchain.

Der Contract ist für das Sepolia Testnetzwerk vorbereitet und wird in der Entwicklungsumgebung [Remix](https://remix.ethereum.org/) getestet. Eine detaillierte Anleitung zur Verwendung und Testung findet sich in [todo/doing]. 

## Aktueller Stand des main.py Skripts (der Schleifendurchlauf in der Main muss noch angepasst werden, ist jetzt erstmal für Testzwecke so wie es ist)

- **Initialisierung**: Das Skript importiert benötigte Bibliotheken und eine Konfigurationsdatei. Das LED wird als Ausgangspin konfiguriert.
- **WLAN-Verbindung**: Es stellt eine Verbindung zum WLAN her, indem es SSID und Passwort aus der Konfigurationsdatei verwendet. Eine Wartezeit ist eingebaut, bis die Verbindung erfolgreich ist.
- **MQTT-Kommunikation**:
  - Ein MQTT-Client wird initialisiert und eine Callback-Funktion für eingehende Nachrichten definiert.
  - Die Callback-Funktion on_message() ermöglicht das Ein- und Ausschalten des LEDs basierend auf den empfangenen MQTT-Nachrichten.
  - Der MQTT-Client verbindet sich mit dem Broker, abonniert einen Kanal für Nachrichten und startet eine Schleife zur Nachrichtenbehandlung.
- **Feedback über MQTT**:
  - Sendet eine Bereitschaftsnachricht, sobald das WLAN und MQTT konfiguriert sind.
  - Während der Hauptfunktionsschleife wird der LED-Status (ein/aus) abwechselnd geändert und der Status wird nach jedem Schritt zurück an den MQTT-Broker gesendet.
- **Main-Schleifensteuerung**:
  - Eine Schleife führt die Ein- und Ausschaltung des LEDs durch, begleitet von Statusmeldungen, und zählt bis zu einer maximalen Anzahl von Durchläufen (30).
  - Nach Beendigung der Schleife sendet das Gerät eine finale Statusmeldung.


------------------------------
## Todo: 
bis 02.12. 18:00 - 19:00 Uhr
- Config.py lokal mit den korrekten Credentials befüllen und dann led-blinking-test.py testen und anschließend main.py testen.
- Über Mosquitto mitschneiden ? 
