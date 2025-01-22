from biedronka.base_client import BaseClient
from biedronka.resources import Stores, Products


class BiedronkaAPI(BaseClient):
    stores: Stores
    products: Products

    def __init__(self, token: str, base_url: str | None = None):
        self._base_url = base_url or "https://api.prod.biedronka.cloud"
        self._token = token

        super().__init__(self._base_url, self._token)

        self.stores = Stores(self)
        self.products = Products(self)