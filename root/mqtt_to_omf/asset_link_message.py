"""
Creates a JSON packet to define links between assets
for creating AF Asset structure
"""


class CreateAssetLinkMessage(object ):
    def __init__(self, source_index, target_index):
        self.asset_link_message = self.create_asset_link_message(source_index, target_index)

    def create_asset_link_message(sourceIndex, targetIndex):
        assetLinkMessage = [{
            "typeid": "__Link",
            "values": [{
                "source": {
                    "typeid": "FirstStaticType",
                    # "index": "_ROOT"
                    "index": sourceIndex
                },
                "target": {
                    "typeid": "FirstStaticType",
                    # "index": "Asset1"
                    # "index": messageTopic
                    "index": targetIndex
                }
            }]
        }]
        return assetLinkMessage
