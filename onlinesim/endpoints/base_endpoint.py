import requests


class BaseEndpoint:
    """
    A base class for interacting with API endpoints.

    :param base_url: Base URL for the API.
    :param api_key: API key for authentication.
    """

    def __init__(self, base_url, api_key: str, language: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.language = language
        self._headers = {}

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

        if self.api_key:
            kwargs["params"] = kwargs.get("params", {})
            kwargs["params"]["api_key"] = self.api_key

        if self.language:
            kwargs["params"] = kwargs.get("params", {})
            kwargs["params"]["lang"] = self.language

        response = requests.request(
            method, url, headers=self._headers, **kwargs
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
