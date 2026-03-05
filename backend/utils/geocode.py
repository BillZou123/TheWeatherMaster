import requests
import os

def get_api_key():
    key = os.getenv("OPENWEATHER_API_KEY")
    if not key:
        raise Exception("OPENWEATHER_API_KEY not set in environment variables")
    return key

OPENWEATHER_API_KEY = get_api_key()


def parse_gps_coordinates(location_str):
    """
    Try to parse GPS coordinates from input string.
    Example: "43.6532,-79.3832"
    Returns (lat, lon) if valid, otherwise None
    """

    try:
        parts = location_str.split(",")

        if len(parts) != 2:
            return None

        lat = float(parts[0].strip())
        lon = float(parts[1].strip())

        # Validate ranges
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon

        return None

    except:
        return None

def geocode_location(location_query):
    """
    Convert a location string → (lat, lon) using OpenWeather Direct Geocoding API.

    The location string is expected to be a city name, optionally with state/country for disambiguation.

    Returns:
        (latitude, longitude)
    """

    url = "http://api.openweathermap.org/geo/1.0/direct"

    if not OPENWEATHER_API_KEY:
        raise Exception("OPENWEATHER_API_KEY not set in environment variables")

    params = {
        "q": location_query,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Geocoding API request failed")

    data = response.json()

    if len(data) == 0:
        raise ValueError("Location not found")

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    return lat, lon




def geocode_zip(zip_code, country_code="CA"):
    """
    Convert ZIP / postal code → (lat, lon) using OpenWeather ZIP Geocoding API.

    Example:
        geocode_zip("M2K0H1", "CA")
        geocode_zip("10001", "US")

    Returns:
        (latitude, longitude)
    """

    url = "http://api.openweathermap.org/geo/1.0/zip"

    params = {
        "zip": f"{zip_code},{country_code}",
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        raise Exception("ZIP geocoding API request failed")

    data = response.json()

    lat = data["lat"]
    lon = data["lon"]

    return lat, lon