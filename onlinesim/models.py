from datetime import datetime
from typing import NamedTuple, Generic, TypeVar, List

from attr import dataclass


class Country(NamedTuple):
    """
    Represents a country with available numbers.

    Attributes:
        country: The country code.
        country_text: The country name in selected language.
        country_original: The original country name.
    """
    country: int
    country_text: str
    country_original: str


class Number(NamedTuple):
    """
    Represents a free number.

    Attributes:
        number: The number.
        country: The country code.
        country_original: The original country name.
        data_humans: Last update time in human-readable format.
        full_number: The full number, i.e. with country code.
        is_archive: Whether the number is archived.
    """
    number: str
    country: int
    country_original: str
    data_humans: str
    full_number: str
    is_archive: bool


class Message(NamedTuple):
    """
    Represents a message.

    Attributes:
        id: The message ID.
        text: The message text.
        in_number: Sender number.
        my_number: The number the message was sent to.
        created_at: The message creation time.
        data_humans: The message creation time in human-readable format.
        code: The message verification code, if message is a verification code.
    """
    id: int
    text: str
    in_number: str
    my_number: int
    created_at: datetime
    data_humans: str
    code: str


T = TypeVar('T')


@dataclass
class PaginatedResponse(Generic[T]):
    """
    Represents a paginated response.

    Attributes:
        data: The data.
        current_page: The current page number.
        total_pages: The total number of pages.
    """
    data: List[T]
    current_page: int
    total_pages: int
