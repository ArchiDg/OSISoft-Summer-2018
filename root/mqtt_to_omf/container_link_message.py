"""
Creates a JSON packet to define links between container
and asset to create attributes with PI point references
using container id properties
"""


class CreateContainerLinkMessage(object):
    def __init__(self, container_source_index, container_id):
        self.containerLinkMessage = \
            self.create_container_link_message(container_source_index, container_id)

    def create_container_link_message(containerSourceIndex, containerid):
        containerLinkMessage = [{
            "typeid": "__Link",
            "values": [{
                "source": {
                    "typeid": "FirstStaticType",
                    "index": containerSourceIndex
                },
                "target": {
                    "containerid": containerid
                }
            }]
        }]
        return containerLinkMessage


