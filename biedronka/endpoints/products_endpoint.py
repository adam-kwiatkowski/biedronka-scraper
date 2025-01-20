from typing import Optional, List

from biedronka.endpoints.base_endpoint import BaseEndpoint
from biedronka.models import ProductStock
from biedronka.types import Proxies


class ProductsEndpoint(BaseEndpoint):
    def __init__(self, base_url: str, token: str, proxies: Optional[Proxies] = None):
        super().__init__(base_url, token, proxies)

    def get_stock_at_store(self, store_code, ean) -> ProductStock:
        """
        Fetches stock information for a specific store and product.

        :param store_code: ID of the store.
        :param ean: EAN of the product.
        :return: Product stock information.
        """
        endpoint = f"/api/v6/products/stock/{store_code}/{ean}/"
        response = self.get(endpoint)

        response.raise_for_status()

        return ProductStock(**response.json())

    def get_stock_at_location(self, lat, lon, ean) -> List[ProductStock]:
        """
        Fetches stock information for a given product at a specific location.

        :param lat: Latitude of the location.
        :param lon: Longitude of the location.
        :param ean: EAN of the product.
        :return: List of product stock information.
        """
        endpoint = "/api/v6/products/stock/"
        payload = {"latitude": lat, "longitude": lon, "ean": ean}
        response = self.post(endpoint, payload)

        response.raise_for_status()

        return [ProductStock(**stock) for stock in response.json()]
