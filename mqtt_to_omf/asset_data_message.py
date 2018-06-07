"""
# Create a JSON packet to define assets for the PI AF asset structure
"""


class CreateAssetMessage(object):
    def __init__(self, index, asset_name):
        self.asset_data_message = self.create_asset_data_message(index, asset_name)

    # Create a JSON packet to define assets
    def create_asset_data_message(index, assetName):
        assetDataMessage = [{
            "typeid": "FirstStaticType",
            "values": [{
                "index": index,
                "name": assetName,
            }]
        }]
        return assetDataMessage
