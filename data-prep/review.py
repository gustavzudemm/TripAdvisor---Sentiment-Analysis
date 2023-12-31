from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class Review(ABC):

    _id: str
    title: str
    text: str
    rating: int
    reviewer_handle: Optional[str]
    language: Optional[str]
    
@dataclass
class TripAdvisorReview(Review):
    
    airline_name: str
    flight_date: str
    flight_connection: str
    flight_type: Optional[str]      # Domestic, International, Europe etc.
    booking_class: Optional[str]    # Economy, Business etc.



