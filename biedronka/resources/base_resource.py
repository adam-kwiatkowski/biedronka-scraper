from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from biedronka.client import BiedronkaAPI


class BaseResource:
    _client: "BiedronkaAPI"
    """
    A base class for interacting with API endpoints.
    """

    def __init__(self, client: "BiedronkaAPI"):
        self._client = client

        self._get = client.get
        self._post = client.post
