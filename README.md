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
bis 20.11. 16:00 - 18:00 Uhr
- Readme aktualisieren
- micropython.py verstehen und je nach chain eintrag die LED setzen und die Aktualisierung über MQTT publishen (idealerweise fügen wir das dann noch sinnvoll ins main ein)
