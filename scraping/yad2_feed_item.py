from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Address:
    city: Optional[str]
    neighborhood: Optional[str]
    floor: Optional[str]
    street: Optional[str] = field(init=False)
    street_number: Optional[int] = field(init=False)
    street_and_number: Optional[str] = field(default="")

    def __post__init__(self):
        if self.street_and_number:
            maybe_number = self.street_and_number.split(" ")[-1]
            if maybe_number.isnumeric():
                self.street_number = int(maybe_number)
                self.street = " ".join(self.street_and_number.split(" ")[:-1])
            else:
                self.street = self.street_and_number
                self.street_number = None


# pylint: disable=too-many-instance-attributes
@dataclass
class FeedItem:
    address: Address = field(hash=True)
    seller_name: str = field(hash=True, default="")
    seller_phone_number: str = field(hash=True, default="")
    estate_type: str = field(hash=True, default="")
    rooms: str = field(hash=True, default="")
    square_meter: str = field(hash=True, default="")
    price: str = field(hash=False, default="")
    updated_date: str = field(hash=False, compare=False, default="")
    description: str = field(hash=False, repr=False, compare=False, default="")
