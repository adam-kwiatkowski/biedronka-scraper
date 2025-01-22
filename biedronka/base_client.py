import requests


class BaseClient:
    def __init__(self, base_url: str, token: str):
        self._base_url = base_url
        self._token = token
        self._default_headers = {"Accept": "application/json", }

    @property
    def base_url(self):
        return self._base_url

    @property
    def _auth_headers(self):
        return {"Authorization": f"Bearer {self._token}"}

    @property
    def _headers(self):
        """
        Headers for HTTP requests.
        """

        return {**self._default_headers, **self._auth_headers}

    def _make_request(self, method, endpoint, **kwargs):
        """
        Handles HTTP requests.
        """
        url = f"{self._base_url}{endpoint}"

        response = requests.request(method, url, headers=self._headers, **kwargs)
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
