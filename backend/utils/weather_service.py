
import requests





def getWeatherFromCoordinates(lat, lon):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "temperature_unit": "celsius"
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        raise Exception(f"Weather API request failed due to {response.text}")

    data = response.json()
    #print(data)

    current = data["current_weather"]

    weather_data = {
        "temperature": current["temperature"],
        "wind_speed": current["windspeed"],
        "wind_direction": current["winddirection"],
        "weather_code": current["weathercode"],
        "is_day": current["is_day"]
    }

    return weather_data



def getWeatherRange(lat, lon, start_date, end_date):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}"
        f"&longitude={lon}"
        f"&start_date={start_date}"
        f"&end_date={end_date}"
        "&daily=temperature_2m_max,temperature_2m_min"
        "&timezone=auto"
    )

    response = requests.get(url)
    data = response.json()

    if "daily" not in data:
        raise ValueError("Weather API failed")

    return {
        "dates": data["daily"]["time"],
        "temperatures": data["daily"]["temperature_2m_max"]
    }