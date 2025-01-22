from typing import List

from biedronka.models import Store
from biedronka.resources.base_resource import BaseResource


class Stores(BaseResource):
    def get_stores(self, lat: float, lon: float, page: int = 1, search: str = "") -> List[Store]:
        """
        Fetches stores based on location and search criteria.

        Args:
            lat (float): Latitude for store search.
            lon (float): Longitude for store search.
            page (int): Page number for pagination.
            search (str): Search term for filtering stores.
        Returns:
            A list of stores based on the location and search criteria.
        """
        endpoint = "/api/v6/store/"
        params = {"lat": lat, "lon": lon, "page": page, "search": search}
        response = self._get(endpoint, params=params)

        response.raise_for_status()

        return [Store(**store) for store in response.json().get("stores", [])]
