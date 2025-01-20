from datetime import datetime
from typing import NamedTuple


class Store(NamedTuple):
    """
    Represents a store.

    Attributes:
        code (str): Unique identifier for the store
        name (str): Store name
        street (str): Street address
        zip_code (str): Postal code
        city (str): City name
        is_in_refurbishment (bool): Whether store is under renovation
        close_date (datetime): Store closing time
        open_date (datetime): Store opening time
        distance (int): Distance in meters from search point
        latitude (float): Geographic latitude coordinate
        longitude (float): Geographic longitude coordinate
        is_sunday_store (bool): Whether store operates on Sundays
        is_closed_now (bool): Whether store is currently closed
        target_hour (datetime): Target operating hours timestamp
    """
    code: str
    name: str
    street: str
    zip_code: str
    city: str
    is_in_refurbishment: bool
    close_date: datetime
    open_date: datetime
    distance: int
    latitude: float
    longitude: float
    is_sunday_store: bool
    is_closed_now: bool
    target_hour: datetime


class ProductStock(NamedTuple):
    """
    Represents product stock information at a specific store.

    Attributes:
        code (str): Store identifier code
        coverage (int): Stock availability level
        distance (int): Distance in meters from search point
        city (str): City name where store is located
        street (str): Street address of the store
    """
    code: str
    coverage: int
    distance: int
    city: str
    street: str
