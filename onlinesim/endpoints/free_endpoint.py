from typing import List

from onlinesim.endpoints.base_endpoint import BaseEndpoint
from onlinesim.models import Country, Number, PaginatedResponse, Message

class FreeEndpoint(BaseEndpoint):
    def __init__(self, base_url: str, api_key: str, language: str):
        super().__init__(base_url, api_key, language)

    def get_countries(self) -> List[Country]:
        """
        Fetches a list of countries with available numbers.

        :return: A list of countries with available numbers.
        """
        endpoint = "/api/getFreeList"
        response = self.get(endpoint)

        response.raise_for_status()

        return [Country(**country) for country in response.json().get("countries", [])]

    def get_numbers(self, country_code: int) -> List[Number]:
        """
        Fetches a list of free numbers for a specific country.

        :param country_code: The country code to fetch numbers for.
        :return: A list of free numbers for the specified country.
        """

        endpoint = "/api/getFreeList"
        params = {"country": country_code}
        response = self.get(endpoint, params=params)

        response.raise_for_status()

        return [Number(number=number, **data) for number, data in response.json().get("numbers", {}).items()]

    def get_messages(self, number: Number = None, page: int = 1) -> PaginatedResponse[Message]:
        """
        Fetches messages.

        :param number: The number to fetch messages for, empty for all numbers.
        :param page: The page number for pagination.
        :return: A paginated response containing messages for the specified number.
        """
        endpoint = "/api/getFreeList"
        params = {"page": page}
        if number:
            params["number"] = number.number
            params["country"] = number.country

        response = self.get(endpoint, params=params)

        response.raise_for_status()

        messages = response.json().get("messages", {}).get("data", [])
        current_page = response.json().get("messages", {}).get("current_page", 1)
        total_pages = response.json().get("messages", {}).get("last_page", 1)

        return PaginatedResponse(
            data=[Message(**message) for message in messages],
            current_page=current_page,
            total_pages=total_pages
        )