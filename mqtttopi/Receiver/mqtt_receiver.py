"""
Create mqtt client and connect to mqtt server.
trigger on_connect after connecting to mqtt server.
Triggers on_message callback upon receiving message from mqtt server
"""

import paho.mqtt.client as mqtt
import datetime
import json
import logging
### MAKE CSV FILE
                       ### HOW TO ADD CONFIG FILE

from mqtttopi.Sender.omf_sender import SendOmfMessageToEndpoint \
    as send_omf_message_to_endpoint
from mqtttopi.mqtt_to_omf.asset_data_message import CreateAssetMessage \
    as create_asset
from mqtttopi.mqtt_to_omf.asset_link_message import CreateAssetLinkMessage \
    as asset_link
from mqtttopi.mqtt_to_omf.container_link_message import CreateContainerLinkMessage \
    as container_link
from mqtttopi.mqtt_to_omf.container_message import CreateContainerMessage \
    as container_message
from mqtttopi.mqtt_to_omf.create_data_value_for_container import CreateDataValueForContainer \
    as create_data_values


class MqttClient(object):
    # Constructor
    def __init__(self, client_name, ip_address, port, topic):
        """
        Creates mqtt client\n
        :param client_name: unique name\n
        :param ip_address: string\n
        :param port: int\n
        :param topic: follows MQTT topic format\n
        """
        self.connected = False
        self.topic = topic
        self.client = mqtt.Client(client_name, clean_session=False)
        self.client.on_connect = self.on_connect
        self.establishConnection(ip_address, port)
        self.client.on_message = self.on_message

    # on_connect callback
    def on_connect(self, client, userdata, flags, rc):
        """
        Function: on_connect
        :param client: MQTT client instance
        :param userdata: private user data
        :param flags: response falgs sent by MQTT server
        :param rc: result code
        """
        if rc == 0:
            self.connected = True
        else:
            print("Connection failed")
            self.client.loop_stop()

        print("on_connect:Connected with flags:{0},result code:{1}".format(flags,
              rc))

    # magic method!
    def __enter__(self):
        """
        Start the mqtt client loop and return self, allows implementing objects
        which can be used easily with the 'with' statement.
        :return: self
        """
        self.client.loop_start()
        return self

    # magic method!
    def __exit__(self, type, value, tb):
        """
        Automatically closes the connection once the corresponding 'with'
        statement goes out of scope
        :param type: type
        :param value: value
        :param tb: tb
        """
        self.client.loop_stop()
        self.client.disconnect()

    # Static method
    def establishConnection(self, address, port):
        try:
            self.client.connect(address, port)
        except _MqttException:
            raise _MqttException("Establishing Connection Failed")

    # on_message callback
    global topics_set
    topics_set = set()
    global asset_set
    asset_set = set()

    def on_message(self, client, userdata, message):
        """
        This is the on_message call back
        :param client: mqtt client
        :param userdata: user data
        :param message: mqtt message
        """
        global messageTopic
        global messagePayload
        global dataValue
        global timestamp
        global topicElement
        global on_message_time  # latency analysis
        global data_value_send_time  # latency analysis
        try:
            # test for unicode decode error
            decodeTest = str(message.payload.decode("utf-8"))
            on_message_time = datetime.datetime.now()  # @@@@@@@@@@@@@@@@@@
            messageTopic = message.topic
            topicElementsList = messageTopic.split("/")
            messagePayload = json.loads(message.payload)
            # returns json object from string
            dataValue = messagePayload['Value']
            timestamp = (messagePayload['Timestamp']) # gives the string
            #timestamp = str(datetime.datetime.now())
            status = (messagePayload['Status'])
            description = (messagePayload['Description'])

            logging.info("ON_MESSAGE, messageTopic: {0},payload: {1},"
                         " at time: {2}\n".format(messageTopic,
                                                  json.dumps(messagePayload, indent=4),
                                                  str(datetime.datetime.now())))
            print("ON_MESSAGE, messageTopic: {0}, payload: {1},"
                  " at time: {2}\n".format(messageTopic,
                                           json.dumps(messagePayload, indent=4),
                                           str(datetime.datetime.now())))
            # json.dumps takes an object and produces a string

            # Checks if the message topic is already in the set. In case it is there,
            # directly sends data value to the container. If it is not there, creates
            # container message, asset, link between assets, link between container
            # and assets, then sends data value to the container
            if messageTopic not in topics_set:
                topics_set.add(messageTopic)

                # Create and send container message
                send_omf_message_to_endpoint("container",
                                             container_message.create_container_message(messageTopic))
                print("CONTAINER message created and sent to end point,at time: {0}".
                      format(str(datetime.datetime.now())))

                ### Creates drop down AF hierarchy ###
                # Create and send Data Messages (Static Data & Link Data)
                for i in range(len(topicElementsList)):
                    if (i == 0):
                        topicElement = topicElementsList[i]  # asset name
                        assetIndex = topicElementsList[i]
                        # Ensure unique index for each asset
                        sourceIndex = "_ROOT"  # needed for link message
                        targetIndex = assetIndex  # needed for link message
                    else:
                        topicElement = topicElementsList[i]
                        prevAssetIndex = assetIndex
                        assetIndex = prevAssetIndex + "/" + topicElementsList[i]
                        sourceIndex = prevAssetIndex  # needed for link message
                        targetIndex = assetIndex  # needed for link message

                    # Make sure each asset is created only once
                    if assetIndex not in asset_set:
                        asset_set.add(assetIndex)
                        # Create and Send assets
                        send_omf_message_to_endpoint("data", create_asset.create_asset_data_message
                        (assetIndex, topicElement))
                        # logging.info("DATA message(asset): sent to define assets,
                        #       at time: {0}".format(str(datetime.datetime.now())))

                        # Create and send link between assets
                        send_omf_message_to_endpoint("data", asset_link.create_asset_link_message
                        (sourceIndex, targetIndex))
                    #  logging.info("DATA message(Link assets): to define link between assets,
                    #                    at time: {0}".format(str(datetime.datetime.now())))

                    else:
                        print("asset and link message already in end point ")

                # Create and send link between container and asstes
                # uses last asset element as source index
                send_omf_message_to_endpoint("data", container_link.create_container_link_message
                (messageTopic, messageTopic))
                # logging.info("DATA message (Link container to asset): to link
                # container to assets,at time: {0}".format(str(datetime.datetime.now())))


                # Send data to containers
                send_omf_message_to_endpoint("data", create_data_values.create_data_values_for_second_dynamic_type
                (messageTopic, dataValue, timestamp, status, description))
                data_value_send_time = datetime.datetime.now()  # @@@@@@@@@@@@@@
                logging.info("Time interval: {}".format(data_value_send_time - on_message_time))
                logging.info("DATA message (DATA VALUE): Values sent to containers")

            else:
                logging.info("Message Topic already in endpoint as CONTAINER:"
                             "{0}".format(messageTopic))

                send_omf_message_to_endpoint("data", create_data_values.create_data_values_for_second_dynamic_type
                (messageTopic, dataValue, timestamp, status, description))
                data_value_send_time = datetime.datetime.now()  # @@@@@@@@@@@@@@
                logging.info("DATA message (DATA VALUE): Values sent to end point to containers\n\n")
                logging.info("Time interval: {}".format(data_value_send_time - on_message_time))

        except:
            client.disconnect()
            client.loop_stop()
            print("Exception happened!")


# private class mqtt exception
class _MqttException(Exception):
    def __init__(self, message):
        if message != None:
            self.message = message
        else:
            self.message= ""

    def __str__(self):
        return self.message