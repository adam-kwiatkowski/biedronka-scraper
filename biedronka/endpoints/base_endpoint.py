from typing import Optional

import requests

from biedronka.types import Proxies


class BaseEndpoint:
    """
    A base class for interacting with API endpoints.

    :param base_url: Base URL for the API.
    :param token: Bearer token for authentication.
    :param proxies: Proxies to use for requests.
    """

    def __init__(self, base_url, token: str, proxies: Optional[Proxies] = None):
        self.base_url = base_url
        self._token = token
        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        self.proxies = proxies

    @property
    def token(self):
        """
        Bearer token for authentication.
        """

        return self._token

    @token.setter
    def token(self, value: str):
        self._token = value
        self._headers["Authorization"] = f"Bearer {self._token}"

    @property
    def headers(self):
        """
        Headers for HTTP requests.
        """

        return self._headers

    @headers.setter
    def headers(self, value: dict):
        self._headers.update(value)

    def _make_request(self, method, endpoint, **kwargs):
        """
        Handles HTTP requests.
        """
        url = f"{self.base_url}{endpoint}"

        response = requests.request(
            method, url, headers=self._headers, proxies=self.proxies, **kwargs
        )
        response.raise_for_status()
        return response

    def get(self, endpoint, params=None):
        """
        Makes a GET request.
        """
        return self._make_request("get", endpoint, params=params)

    def post(self, endpoint, payload):
        """
        Makes a POST request.
        """
        return self._make_request("post", endpoint, json=payload)
