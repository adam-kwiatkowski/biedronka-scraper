from typing import Optional

from biedronka.endpoints.products_endpoint import ProductsEndpoint
from biedronka.endpoints.stores_endpoint import StoresEndpoint
from biedronka.types import Proxies


class BiedronkaAPI:
    def __init__(self, token: str, proxies: Optional[Proxies] = None):
        self._base_url = "https://api.prod.biedronka.cloud"
        self._token = token
        self._proxies = proxies

        self._endpoints = {
            "stores": StoresEndpoint(self._base_url, self._token, self._proxies),
            "products": ProductsEndpoint(self._base_url, self._token, self._proxies),
        }

    @property
    def token(self):
        """
        Bearer token for authentication.
        """

        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value
        for endpoint in self._endpoints.values():
            endpoint.token = value

    @property
    def proxies(self):
        """
        Proxies to use for requests.
        """

        return self._proxies

    @proxies.setter
    def proxies(self, value: Optional[Proxies]):
        self._proxies = value
        for endpoint in self._endpoints.values():
            endpoint.proxies = value

    @property
    def stores(self):
        return self._endpoints["stores"]

    @property
    def products(self):
        return self._endpoints["products"]
