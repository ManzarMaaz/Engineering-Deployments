# flight_data.py
from dataclasses import dataclass

@dataclass
class FlightData:
    """
    A simple data model representing a potential flight deal found in the sheet.
    """
    city_name: str
    iata_code: str
    target_price: float
    cheapest_price: float = None  # To be filled after the flight search API call
    row_id: int = None
    stops: int = 0