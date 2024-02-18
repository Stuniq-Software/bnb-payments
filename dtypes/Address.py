from typing import Optional


class Address:
    line1: str
    line2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str

    def __init__(self):
        self.line1 = ""
        self.line2 = None
        self.city = ""
        self.state = ""
        self.postal_code = ""
        self.country = ""

    @staticmethod
    def from_tuple(address_tuple: tuple):
        address = Address()
        address.line1 = address_tuple[1]
        address.line2 = address_tuple[2]
        address.city = address_tuple[3]
        address.state = address_tuple[4]
        address.postal_code = address_tuple[5]
        address.country = address_tuple[6]
        return address

    def to_dict(self) -> dict:
        return {
            "line1": self.line1,
            "line2": self.line2,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country
        }