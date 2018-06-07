"""
This class is used for sending an HTTPS message (web request messages)
All it does is take in a data object and a message type, and it sends an HTTPS
request to the target OMF endpoint
"""
import json
import datetime
import gzip
import requests


class SendOmfMessageToEndpoint(object):

    # Constructor
    def __init__(self, message_type, message_omf_json):
        # Specify whether to compress OMF message before
        # sending it to ingress endpoint
        USE_COMPRESSION = True
        # If self-signed certificates are used (true by default),
        # do not verify HTTPS SSL certificates; normally, leave this as is
        VERIFY_SSL = False
        # Specify the timeout, in seconds, for sending web requests
        # (if it takes longer than this to send a message, an error will be thrown)
        WEB_REQUEST_TIMEOUT_SECONDS = 30
        # Specify options for sending web requests to the target PI System
        PRODUCER_TOKEN = "uid=160c1583-f721-41c4-bccf-f74c68ddd894&crt=20180604181656275&sig=RZRx2d2yi6C5VzA6vqr7BvZeY/3RTjWr2GnuGYMIjC4="
        INGRESS_URL = "https://loanersurface4.osisoft.int:5460/ingress/messages"

        try:
            # Compress json omf payload, if specified
            compression = 'none'
            if USE_COMPRESSION:
                msg_body = gzip.compress(bytes(json.dumps(message_omf_json), 'utf-8'))
                compression = 'gzip'
            else:
                msg_body = json.dumps(message_omf_json)
            # Assemble headers
            msg_headers = {
                'producertoken': PRODUCER_TOKEN,
                'messagetype': message_type,
                'action': 'create',
                'messageformat': 'JSON',
                'omfversion': '1.0',
                'compression': compression
            }

            # Send the request, and collect the response
            response = requests.post(
                INGRESS_URL,
                headers=msg_headers,
                data=msg_body,
                verify=VERIFY_SSL,
                timeout=WEB_REQUEST_TIMEOUT_SECONDS
            )

            # Turn off HTTPS warnings, if an untrusted certificate is used by
            # the target endpoint
            # Remove if targetting trusted targets
            if not VERIFY_SSL:
                requests.packages.urllib3.disable_warnings()

            # Print a debug message, if desired; note: you should receive a
            # response code 204 if the request was successful!
            print('\nResponse from relay from the initial "{0}" message: {1} {2} {3}'.format
                  (message_type, response.status_code, response.text, str(datetime.datetime.now())))
        except Exception as e:
            print(str(datetime.datetime.now()) + " An error ocurred during web request: " + str(e))


