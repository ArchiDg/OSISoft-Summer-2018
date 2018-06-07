"""
Send the types messages to define the types of streams that will be sent.
These types are referenced in all later messages
Sends a JSON packet to define static and dynamic types
"""
from mqtttopi.Sender.omf_sender import SendOmfMessageToEndpoint as send_omf_message_to_endpoint


class SendTypeMessage(object):

    def __init__(self):
        send_omf_message_to_endpoint("type", [
            {
                "id": "FirstStaticType",
                "name": "First static type",
                "classification": "static",
                "type": "object",
                "description": "First static asset type",
                "properties": {
                    "index": {
                        "type": "string",
                        "isindex": True,
                        "name": "not in use",
                        "description": "not in use"
                    },
                    "name": {
                        "type": "string",
                        "isname": True,
                        "name": "not in use",
                        "description": "not in use"
                    }
                }
            }, {
                "id": "SecondDynamicType",
                "name": "Second dynamic type",
                "classification": "dynamic",
                "type": "object",
                "description": "not in use",
                "properties": {
                    "timestamp": {
                        "format": "date-time",
                        "type": "string",
                        "isindex": True,
                        "name": "not in use",
                        "description": "not in use"
                    },
                    "NumberProperty1": {
                        "type": "number",
                        "name": "Value",
                        "description": "PI point data value sent by device/sensor",
                        "format": "float64"
                    },
                    "Property2": {
                        "type": "string",
                        "name": "Timestamp",
                        "description": "Timestamp sent by the sensor/device",
                        "format": "date-time"
                    },
                    "StringEnum": {
                        "type": "string",
                        "enum": ["False", "True", "Open", "Close", "On", "Off"],
                        "name": "Status",
                        "description": "String enumeration to describe status of the device"
                    },
                    "Description": {
                        "type": "string",
                        "name": "Description",
                        "description": "Dynamic asset's attribute description"
                    }
                }
            }
        ])
