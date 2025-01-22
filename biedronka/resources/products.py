from typing import List

from biedronka.models import ProductStock
from biedronka.resources.base_resource import BaseResource


class Products(BaseResource):
    def get_stock_at_store(self, store_code: str, ean: str) -> ProductStock:
        """
        Fetch stock information for a specific store and product.

        Args:
            store_code (str): The store code.
            ean (str): The EAN of the product.

        Returns:
            The stock information for the product at the store.
        """
        endpoint = f"/api/v6/products/stock/{store_code}/{ean}/"
        response = self._get(endpoint)

        response.raise_for_status()

        return ProductStock(**response.json())

    def get_stock_at_location(self, lat, lon, ean) -> List[ProductStock]:
        """
        Fetch stock information for a given product at a specific location.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.
            ean (str): The EAN of the product.

        Returns:
            A list of stock information for the product at the location.
        """
        endpoint = "/api/v6/products/stock/"
        payload = {"latitude": lat, "longitude": lon, "ean": ean}
        response = self._post(endpoint, payload)

        response.raise_for_status()

        return [ProductStock(**stock) for stock in response.json()]
