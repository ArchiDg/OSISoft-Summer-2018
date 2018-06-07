"""
This is the Main class that creates an instance of the MqttClient class with
specified name, mqtt server address, port number and topic.
"""
import time
from mqtttopi.Receiver.mqtt_receiver import MqttClient
from mqtttopi.mqtt_to_omf.send_type_message import SendTypeMessage

client_name = "receiver1"
ip_address = "127.0.0.1"
port_num = 1883
topic_name = "F_HAUS_11/#"
counter = 0

# send the type message to relay once in the beginning of the application
SendTypeMessage()

with MqttClient(client_name, ip_address, port_num, topic_name) as f:
    if f.connected is False:
        time.sleep(0.5)
    try:
        while f.connected:
            f.client.subscribe(f.topic)
            #print("connected: " + str(counter))
            time.sleep(0.000005)
            counter += 1

    except KeyboardInterrupt:  # why doesn't it work ???
        print("Keyboard Interrupt")
        pass

# TODO: create some logic to make sure that the while loop ends/client disconnects at some point
