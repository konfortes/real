from dataclasses import dataclass


@dataclass
class Address:
    city: str = ""
    # TODO: separate street and number
    street_and_number: str = ""
    neighborhood: str = ""
    floor: str = ""


# pylint: disable=too-many-instance-attributes
@dataclass
class FeedItem:
    address: Address
    seller_name: str = ""
    seller_phone_number: str = ""
    estate_type: str = ""
    rooms: str = ""
    square_meter: str = ""
    price: str = ""
    updated_date: str = ""
    description: str = ""
