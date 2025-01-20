import json

from biedronka.api import BiedronkaAPI

if __name__ == "__main__":
    with open("config.json") as f:
        config = json.load(f)

    api = BiedronkaAPI(token=config.get("token"))

    stores = api.stores.get_stores(lat=52.22977, lon=21.01178)

    store = stores[0]

    print(store.name)

    coverage = api.products.get_stock_at_store(store.code, ean="5063270101797")

    print(coverage)

    location_coverage = api.products.get_stock_at_location(lat=52.22977, lon=21.01178, ean="5063270101797")
    location_coverage.sort(key=lambda x: x.coverage, reverse=True)

    for stock in location_coverage:
        print(f"{stock.street}: {stock.coverage}")
