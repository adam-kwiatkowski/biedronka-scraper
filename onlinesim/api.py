from typing import Union, Optional

from onlinesim.endpoints.free_endpoint import FreeEndpoint


class OnlineSimAPI:
    free: FreeEndpoint

    def __init__(self, api_key: str = None, language: str = "en"):
        self._api_key = api_key
        self._base_url ="https://onlinesim.io"
        self._language = language

        self.free = FreeEndpoint(self._base_url, self._api_key, self._language)

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value
        self.free.api_key = value

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value
        self.free.language = value