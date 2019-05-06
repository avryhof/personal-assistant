import logging
import os

from wit import Wit

wit_access_token = os.environ.get('WIT_ACCESS_TOKEN')

client = Wit(wit_access_token)
client.logger.setLevel(logging.INFO)

resp = client.message('bedtime story')

print('Yay, got Wit.ai response: ' + str(resp))

