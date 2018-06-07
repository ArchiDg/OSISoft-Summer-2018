"""
This Container message creates a container by defining container ids and the type
(using the types listed in the "send_type_message.py") for each new data events
container.
We can now directly start sending data to it using its Id.
"""


class CreateContainerMessage(object):
    def __init__(self, container_id):
        self.container = self.create_container_message(container_id)


    # CONTAINER message - creates containers
    def create_container_message(containerID):
        container = [{
            # "id": "Container3",
            "id": containerID,
            "typeid": "SecondDynamicType"
        }]
        return container

