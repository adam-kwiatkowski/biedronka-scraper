import json
import time
import requests
import pandas as pd
from rich.progress import track
import logging
from requests.exceptions import RequestException, Timeout

# Set up logging
logging.basicConfig(level=logging.WARNING)

class ProxySwitchReason:
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"
    FRESH = "FRESH"

class ProxyProvider:
    """
    A class for providing proxies from a list. Keeps track of when a proxy was last used.
    """

    def __init__(self, proxies):
        self.proxies = [{"proxy": proxy, "last_used": 0, "switch_reason": ProxySwitchReason.FRESH} for proxy in proxies]
        self.current_proxy = self.proxies[0]

    def get_proxy(self):
        """
        Returns the current proxy and updates the last used timestamp.
        """
        if self.current_proxy["switch_reason"] != ProxySwitchReason.FRESH:
            logging.warning(f"This proxy was switched before due to {self.current_proxy['switch_reason']}")

        self.current_proxy["last_used"] = time.time()

        return self.current_proxy["proxy"]
    
    def switch_proxy(self, switch_reason):
        """
        Switches to the next proxy in the list and updates the switch reason.
        """
        self.current_proxy["last_used"] = 0
        self.current_proxy["switch_reason"] = switch_reason
        self.proxies.append(self.proxies.pop(0))
        self.current_proxy = self.proxies[0]

class BaseEndpoint:
    """
    A base class for interacting with API endpoints with proxy resilience.
    """

    def __init__(self, base_url, headers=None, proxy_provider: ProxyProvider = None):
        self.base_url = base_url
        self.headers = headers or {}
        self.proxy_provider = proxy_provider

    def set_headers(self, headers):
        self.headers.update(headers)

    def _make_request(self, method, endpoint, **kwargs):
        """
        Handles HTTP requests with retry logic and proxy resilience.
        """
        url = f"{self.base_url}{endpoint}"
        attempt = 0
        max_retries = len(self.proxy_provider.proxies) if self.proxy_provider else 3

        while attempt < max_retries:
            try:
                proxy = (
                    self.proxy_provider.get_proxy()
                    if self.proxy_provider
                    else None
                )
                logging.info(f"Attempting {method.upper()} request to {url} with proxy: {proxy}")
                response = requests.request(
                    method, url, headers=self.headers, proxies=proxy, timeout=10, **kwargs
                )
                response.raise_for_status()

                if response.status_code == 404:
                    # Graceful handling of 404 errors without switching the proxy
                    logging.warning(f"404 Not Found for {url}. Proceeding without switching proxy.")
                    return None

                return response
            except Timeout:
                logging.warning(f"Request to {url} timed out. Switching proxy.")
                if self.proxy_provider:
                    self.proxy_provider.switch_proxy(ProxySwitchReason.TIMEOUT)
                attempt += 1
            except RequestException as e:
                if hasattr(e.response, 'status_code') and e.response.status_code == 404:
                    # Graceful handling of 404 errors
                    logging.warning(f"404 Not Found for {url}. Proceeding without switching proxy.")
                    return None
                else:
                    logging.error(f"Error during {method.upper()} request to {url}: {e}")
                    if self.proxy_provider:
                        self.proxy_provider.switch_proxy(ProxySwitchReason.ERROR)
                    attempt += 1

        raise RequestException(f"Failed to complete {method.upper()} request to {url} after {max_retries} attempts.")


    def get(self, endpoint, params=None):
        """
        Makes a GET request with retry logic.
        """
        return self._make_request("get", endpoint, params=params)

    def post(self, endpoint, payload):
        """
        Makes a POST request with retry logic.
        """
        return self._make_request("post", endpoint, json=payload)


class StoresEndpoint(BaseEndpoint):
    """
    A class for interacting with the Stores API endpoint.
    """

    def __init__(self, base_url, headers=None, proxy_provider: ProxyProvider=None):
        super().__init__(base_url, headers, proxy_provider)

    def get_stores(self, lat, lon, page=1, search=""):
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
        return response.json()


class StoreStockEndpoint(BaseEndpoint):
    """
    A class for interacting with the Store Stock API endpoint.
    """

    def __init__(self, base_url, headers=None, proxy_provider: ProxyProvider=None):
        super().__init__(base_url, headers, proxy_provider)

    def get_store_stock(self, store_id, ean):
        """
        Fetches stock information for a specific store and product.

        :param store_id: ID of the store.
        :param ean: EAN of the product.
        :return: The JSON response containing stock data.
        """
        endpoint = f"/api/v6/products/stock/{store_id}/{ean}/"
        response = self.get(endpoint)
        return response.json()


class StockEndpoint(BaseEndpoint):
    """
    A class for interacting with the Stock API endpoint.
    """

    def __init__(self, base_url, headers=None, proxy_provider: ProxyProvider=None):
        super().__init__(base_url, headers, proxy_provider)

    def get_stock(self, lat, lon, ean):
        """
        Fetches stock information for a given product and store.

        :param lat: Latitude of the store location.
        :param lon: Longitude of the store location.
        :param ean: EAN of the product.
        :param user_store: Store code.
        :return: The JSON response containing stock data.
        """
        endpoint = "/api/v6/products/stock/"
        payload = {"latitude": lat, "longitude": lon, "ean": ean}
        response = self.post(endpoint, payload)
        return response.json()


class PriceEndpoint(BaseEndpoint):
    """
    A class for interacting with the Price API endpoint.
    """

    def __init__(self, base_url, headers=None, proxy_provider: ProxyProvider=None):
        super().__init__(base_url, headers, proxy_provider)

    def get_price(self, store_id, ean):
        """
        Fetches price information for a specific product in a store.

        :param store_id: ID of the store.
        :param ean: EAN of the product.
        :return: The JSON response containing price data.

        Example response:
        {'theme_name': 'SuperPriceInOut', 'name': 'HERBATA LIPTON SMAKOWA MIX 20 PIRAMIDEK', 'unit': 'za opa', 'unit_price': ['0,35 zł/szt'], 'price': '6.99', 'promotion_valid_period': None, 'details': '', 'limit_message': None, 'only_with_biedronka_card': False, 'regular_price': '6.99', 'is_promotion': False, 'is_minimal_basket_value_bonus_buy': False, 'discount': None, 'price_tag_info': 'SUPERCENA', 'omnibus_price': '0.00', 'discount_to_omnibus_price': None, 'omnibus_type': None, 'description': '', 'type_of_wine': None, 'sweetness_of_wine': None, 'country_of_origin': None, 'product_additional_country_of_origin_info': False, 'fruits_or_vegetables_class': None, 'image_url': 'https://s7e5a.scene7.com/is/image/jeronimomartins/blank', 'thumb_url': 'https://s7e5a.scene7.com/is/image/jeronimomartins/blank', 'multipack': None, 'is_multipack': False, 'badges': []}
        """
        endpoint = f"/api/v6/products/price/{store_id}/{ean}/"
        response = self.get(endpoint)
        return response.json() if response else None


class StoresScraper:
    """
    A class for scraping store data from the StoresEndpoint and saving it using pandas.
    """
    all_stores = None

    def __init__(self, stores_endpoint, max_pages=None):
        self.stores_endpoint = stores_endpoint
        self.max_pages = max_pages

    def fetch_all_stores(self, lat, lon):
        """
        Fetches all stores data by iterating through all pages with a progress bar.
        Allows setting a page limit (max_pages).
        
        :param lat: Latitude for store search.
        :param lon: Longitude for store search.
        :param max_pages: Maximum number of pages to fetch (optional).
        :return: A list of all stores.
        """
        # Fetch the first page to determine the total number of pages
        self.all_stores = []
        first_page_data = self.stores_endpoint.get_stores(lat=lat, lon=lon, page=1)
        total_pages = first_page_data.get("page_count", 0)
        self.all_stores = first_page_data.get("stores", [])

        # Set the maximum number of pages to scrape
        if self.max_pages:
            total_pages = min(total_pages, self.max_pages)

        # Fetch remaining pages with a progress bar
        for page in track(
            range(2, total_pages + 1), description=f"Fetching store data ({total_pages} pages)"
        ):
            data = self.stores_endpoint.get_stores(lat=lat, lon=lon, page=page)
            self.all_stores.extend(data.get("stores", []))

        return self.all_stores

    def save_to_csv(self, stores, filename):
        """
        Saves the store data to a CSV file using pandas.

        :param stores: A list of store dictionaries.
        :param filename: The name of the CSV file to save.
        """
        df = pd.DataFrame(stores)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Data saved to {filename}")


class ProductInfoScraper:
    """
    A class for scraping product information for given stores from the PriceEndpoint.
    Allows filtering stores by code,name,street,zip_code,city,is_in_refurbishment,close_date,open_date,distance,latitude,longitude,is_sunday_store,is_closed_now,target_hour
    """

    def __init__(self, stores_scraper, price_endpoint):
        self.stores_scraper = stores_scraper
        self.price_endpoint = price_endpoint

    def fetch_product_info(self, ean, store_filter=None):
        """
        Fetches product information for a given EAN and store filter.

        :param ean: EAN of the product.
        :param store_filter: A dictionary of store filters.
        :return: A list of product information for the given EAN.
        """
        product_info = []
        if self.stores_scraper.all_stores is None:
            print("Fetching store data...")
            self.stores_scraper.fetch_all_stores(lat=52.237049, lon=21.017532)

        stores_df = pd.DataFrame(self.stores_scraper.all_stores)
        if store_filter:
            for key, value in store_filter.items():
                stores_df = stores_df[stores_df[key] == value]

        for store_id in track(stores_df["code"], description="Fetching product info..."):
            try:
                data = self.price_endpoint.get_price(store_id=store_id, ean=ean)
                if data:
                    product_info.append(data)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching product info for store {store_id}: {e}")

        return product_info

class BiedronkaAPI:
    def __init__(self, base_url, headers=None, proxy_provider: ProxyProvider=None):
        self.base_url = base_url
        self.headers = headers
        self.proxy_provider = proxy_provider
        
        self.update_endpoints()

    def update_endpoints(self):
        self.stores = StoresEndpoint(self.base_url, self.headers, self.proxy_provider)
        self.stock = StockEndpoint(self.base_url, self.headers, self.proxy_provider)
        self.price = PriceEndpoint(self.base_url, self.headers, self.proxy_provider)

# Usage example:
if __name__ == "__main__":
    BASE_URL = "https://api.prod.biedronka.cloud"
    
    with open("config.json") as f:
        config = json.load(f)

    headers = config.get("headers")
    proxies = config.get("proxies")
    proxy_provider = ProxyProvider(proxies)

    api = BiedronkaAPI(base_url=BASE_URL, headers=headers, proxy_provider=proxy_provider)

    try:
        stores_scraper = StoresScraper(stores_endpoint=api.stores, max_pages=1)    
        data = stores_scraper.fetch_all_stores(lat=52.237049, lon=21.017532)

        product_info = api.price.get_price(store_id=data[0]["code"], ean="5901234123458")
        print(product_info)
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
