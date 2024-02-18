from typing import List, Optional
from .Address import Address


class Stay:
    stay_id: str
    host_id: str
    address: Address
    name: str
    description: str
    price_per_night: float
    max_guests: int
    num_bedrooms: int
    area: float
    num_bathrooms: int
    rules: List[str]
    amenities: List[str]
    pictures: List[str]
    lat: float
    long: float
    is_available: bool
    booked_by: Optional[str]
    booked_until: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]

    def __init__(self):
        self.stay_id = ""
        self.host_id = ""
        self.address = Address()
        self.name = ""
        self.description = ""
        self.price_per_night = 0.0
        self.max_guests = 0
        self.num_bedrooms = 0
        self.area = 0.0
        self.num_bathrooms = 0
        self.rules = []
        self.amenities = []
        self.pictures = []
        self.lat = 0.0
        self.long = 0.0
        self.is_available = True
        self.booked_by = None
        self.booked_until = None
        self.created_at = None
        self.updated_at = None

    @staticmethod
    def from_tuple(stay_tuple: tuple):
        stay = Stay()
        stay.stay_id = stay_tuple[0]
        stay.host_id = stay_tuple[1]
        stay.name = stay_tuple[2]
        stay.description = stay_tuple[3]
        stay.price_per_night = stay_tuple[5]
        stay.max_guests = stay_tuple[6]
        stay.num_bedrooms = stay_tuple[7]
        stay.area = stay_tuple[8]
        stay.num_bathrooms = stay_tuple[9]
        stay.rules = stay_tuple[10]
        stay.amenities = stay_tuple[11]
        stay.pictures = stay_tuple[12]
        stay.lat = stay_tuple[13]
        stay.long = stay_tuple[14]
        stay.is_available = stay_tuple[15]
        stay.booked_by = stay_tuple[16]
        stay.booked_until = stay_tuple[17]
        stay.created_at = stay_tuple[18]
        stay.updated_at = stay_tuple[19]
        stay.address = Address.from_tuple(stay_tuple[20:])
        return stay

    def to_dict(self):
        return {
            "stay_id": self.stay_id,
            "host_id": self.host_id,
            "address": self.address.to_dict(),
            "name": self.name,
            "description": self.description,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "num_bedrooms": self.num_bedrooms,
            "area": self.area,
            "num_bathrooms": self.num_bathrooms,
            "rules": self.rules,
            "amenities": self.amenities,
            "pictures": self.pictures,
            "lat": self.lat,
            "long": self.long,
            "booked_by": self.booked_by,
            "booked_until": self.booked_until,
            "is_available": self.is_available,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
