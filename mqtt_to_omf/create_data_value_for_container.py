"""
Creates a JSON packet containing data values for containers of type
'SecondDynamicType' (defined in the type message in "send_type_message.py")
"""


class CreateDataValueForContainer(object):
    def __init__(self, container_id, value, timestamp, status, description):
        self.data_value = self.create_data_values_for_second_dynamic_type\
            (container_id, value, timestamp, status, description)

    def create_data_values_for_second_dynamic_type(containerid, value, timestamp,
                                                   status, description):
        return [
            {
                "containerid": containerid,
                "values": [
                    {
                        # "timestamp": getCurrentTime(),
                        "timestamp": timestamp,  # needs to be in date-time format#
                        "NumberProperty1": value,
                        "Property2": timestamp,
                        "StringEnum": status,
                        "Description": description
                    }
                ]
            }
        ]


