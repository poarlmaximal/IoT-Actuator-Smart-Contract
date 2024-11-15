def main():
    connect_wifi()
    connect_mqtt()
    mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is ready.")
    
    # Zähler für die Durchläufe
    loop_count = 0
    max_loops = 15  # Maximale Anzahl an Schleifendurchläufen
    
    while loop_count < max_loops:
        led.value(1)  # LED einschalten
        mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is on.")
        time.sleep(5)  # 5 Sekunden warten
        
        led.value(0)  # LED ausschalten
        mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} is off.")
        time.sleep(5)  # 5 Sekunden warten
        
        # Zähler erhöhen
        loop_count += 1
    
    # Nach 15 Durchläufen: Statusmeldung und Programmende
    mqtt_client.publish(f"iot/{config.DEVICE_NAME}/status", f"{config.DEVICE_NAME} has stopped after {max_loops} cycles.")
    print("Programm beendet.")
