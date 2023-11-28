import logging

import requests

from okapi.client import config
from okapi.client.client_base import BaseClient
from okapi.core.models import Flag, Activation


class RemoteClient(BaseClient):
    def get_flag_by_name(self, flag_name: str) -> Flag:
        flags_root_url = config.get('remote', 'url')
        url = f"{flags_root_url}/{flag_name}"
        resp = requests.get(url)
        if resp.status_code == requests.codes.ok:
            flag_json = resp.json()
            flag = Flag(**flag_json)
            activations = list(map(lambda activation_json: Activation(**activation_json), flag_json['activations']))
            flag.activations = activations
            logging.getLogger(__name__).debug(flag)
            return flag
