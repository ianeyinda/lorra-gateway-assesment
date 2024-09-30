#!/usr/bin/env python3
# application that usese MQTT to request an IP address

# importing the necessary libraries
import paho.mqtt.client as mqtt
import netifaces as ni
import time


# MQTT broker settings
broker = "broker.emqx.io"
port = 1883
topic = "lora_gateway_ip"

# creating the MQTT client instance
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker!")

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker. Reconnecting...")
    client.reconnect()


# Setting up MQTT callbacks
client.on_connect = on_connect
client.on_disconnect = on_disconnect


while True:
        try:
                #Connecting to the MQTT broker
                client.connect(broker, port)
                break
        except ConnectionRefusedError:
               
               print("Failed to connect to MQTT broker. Retrying in 5 seconds")
               time.sleep(5)


print("Connected to MQTT broker!")


# Getting the IP address assigned to the wifie inerface
wifi_interface = "wlan0"  # Replace with your WiFi interface name of you machine 
try:
    ip_address = ni.ifaddresses(wifi_interface)[ni.AF_INET][0]['addr']
    print("IP address:", ip_address)
except ValueError:
    print("Failed to read IP address from WiFi interface")
    exit(1)
print("IP address:", ip_address)

# Publish the IP address to the MQTT broker
try:
    client.publish(topic, ip_address)
    print("IP address sent to MQTT broker!")
except Exception as e:
    print("Failed to send IP address to MQTT broker:", e)


# keeping the connection alive
while True:
    client.loop()
    time.sleep(1)





