import os
from typing import Tuple
import requests

BASE_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


class GeoCodeException(Exception):
    pass


class GeoCoder:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def get_lat_lng(self, address: str) -> Tuple[float, float]:
        full_url = f"{BASE_API_URL}?address={address}&key={self.api_key}"
        response = requests.get(full_url, timeout=1)
        data = response.json()

        if data["status"] != "OK":
            raise GeoCodeException(
                f"Could not geocode address {address}. Status: {data['status']}"
            )

        location_data = data["results"][0]["geometry"]["location"]

        return location_data["lat"], location_data["lng"]


if __name__ == "__main__":
    key = os.environ["GOOGLE_MAPS_API_KEY"]
    geo_coder = GeoCoder(key)

    demo_address = "משה סנה 5 תל אביב"  # pylint: disable=invalid-name

    lat, lng = geo_coder.get_lat_lng(demo_address)

    print(f"{lat=}, {lng=}")
