import requests
from common.protocol import mcp_response

API_URL = "https://api.open-meteo.com/v1/forecast"

def get_weather(city):
    city_coords = {
        "delhi": (28.61, 77.20),
        "mumbai": (19.07, 72.87),
        "bangalore": (12.97, 77.59)
    }

    if city.lower() not in city_coords:
        return mcp_response("error", "City not supported")

    lat, lon = city_coords[city.lower()]

    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }

    res = requests.get(API_URL, params=params).json()
    temp = res["current_weather"]["temperature"]

    alert = None
    if temp > 35:
        alert = "🔥 Heat Alert!"
    elif temp < 10:
        alert = "❄️ Cold Alert!"

    return mcp_response(
        "success",
        {
            "city": city,
            "temperature": temp,
            "alert": alert
        }
    )


def handle_request(mcp_message):
    if mcp_message["tool"] == "weather":
        return get_weather(mcp_message["params"]["city"])

    return mcp_response("error", "Unknown tool")
