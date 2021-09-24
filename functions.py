from typing import Any, Tuple, Union, TypedDict
from typeguard import check_type

from pathlib import Path

from ast import literal_eval as make_tuple  # Needed to parse string to tuple

from shapely.geometry import Polygon, Point

from requests import get

from icecream import ic

Coords = Tuple[float, float]


class Response(TypedDict):
    text: str
    value: int


def coors_handle(response: dict) -> dict:
    """
    Prevent CORS problems after each request
    :param response: Response of any request
    :return: The same request
    """
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE, PATCH')
    return response


def is_in_mkad(coords: Coords) -> bool:
    """
    Function: is_in_mkad
    Summary: Check if coords are inside of mkad_coords
    Attributes: 
        @param (coords:Coords): Tuple of coords like (0, 0)
    Returns: Bool
    """
    check_type('coords', coords, Coords)  # Will raise an TypeError exception
    # Read file and parse the content as nested tuple
    mkad_coords = make_tuple((Path.cwd() / 'makd_coords.txt').read_text())
    mkad_polygon = Polygon(mkad_coords)  # Make polygon
    # Check if point is inside into MKAD
    return mkad_polygon.contains(Point(coords))


def coords_from_address(address: str) -> Union[Tuple[Coords, str], None]:
    """
    Function: coords_from_address
    Summary: Get coords using google maps geocoding for an address and also get googles place_id
    Examples: Get coords of mexico, city
    Attributes: 
        @param (address:str): Addres in plain text 
    Returns: (Coords, place_id) or None if it fails
    """
    check_type('address', address, str)  # Will raise an TypeError exception
    url = r'https://maps.googleapis.com/maps/api/geocode/json'
    key = (Path.cwd() / 'google.key').read_text()
    if (response := get(url, params=dict(key=key, address=address))
        ).status_code == 200 and response.json()['status'] == 'OK':
        coords = tuple(response.json()['results'].pop()[
                       'geometry']['location'].values())   # Return the coords
        place_id = response.json()['results'][0]['place_id']
        return coords, place_id
    else:
        return None  # And error occurre with the address


def get_distance(place_id: str) -> Union[Response, None]:
    """
    Function: get_distance
    Summary: Meassure distance using google maps api from a place_id to MKAD
    Examples: Distance from Rumania to MKAD
    Attributes: 
        @param (place_id:str): google maps place_id 
    Returns: distance: {'text': str, 'value': int} or None if it fails
    """
    check_type('place_id', place_id, str)  # Will raise an TypeError exception
    url = r'https://maps.googleapis.com/maps/api/distancematrix/json'
    key = (Path.cwd() / 'google.key').read_text()
    destinations = 'MKAD'
    origins = f'place_id:{place_id}'
    if (response := get(url, params=dict(key=key, origins=origins, destinations=destinations))).status_code == 200 \
            and response.json()['status'] == 'OK' \
            and response.json()['rows'][0]['elements'][0]['status'] != 'ZERO_RESULTS':
        return response.json()['rows'][0]['elements'][0]['distance']
    else:
        None
