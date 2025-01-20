from typing import List, Optional

from biedronka.endpoints.base_endpoint import BaseEndpoint
from biedronka.models import Store
from biedronka.types import Proxies


class StoresEndpoint(BaseEndpoint):
    def __init__(self, base_url: str, token: str, proxies: Optional[Proxies] = None):
        super().__init__(base_url, token, proxies)

    def get_stores(self, lat: float, lon: float, page: int = 1, search: str = "") -> List[Store]:
        """
        Fetches stores based on location and search criteria.

        :param lat: Latitude for store search.
        :param lon: Longitude for store search.
        :param page: Page number for pagination.
        :param search: Search term for filtering stores.
        :return: The JSON response containing store data.
        """
        endpoint = "/api/v6/store/"
        params = {"lat": lat, "lon": lon, "page": page, "search": search}
        response = self.get(endpoint, params=params)

        response.raise_for_status()

        return [Store(**store) for store in response.json().get("stores", [])]
