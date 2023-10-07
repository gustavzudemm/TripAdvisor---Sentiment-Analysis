from abc import ABC
from dataclasses import dataclass
from typing import Optional


@dataclass
class Review:

    title: str
    text: str
    rating: int
    reviewer_handle: Optional[str]
    language: Optional[str]
    
@dataclass
class TripAdvisorReview(Review):
    
    flight_date: str
    flight_type: str            # Domestic, Europe, International etc.
    flight_connection: str      # Start - Destination
    booking_class: Optional[str]          # Econonmy, Business, First Class



