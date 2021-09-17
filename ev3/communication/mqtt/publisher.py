#!/usr/bin/env python3

import paho.mqtt.client as mqtt

HOST = "10.0.0.13"
TOPIC = "topic/test"

client = mqtt.Client()
client.connect(HOST)


def publish_message(payload):
    client.publish(TOPIC, payload)


client.disconnect()
