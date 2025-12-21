import requests
from datetime import datetime, timezone

# Fetch geographic coordinates for a given city
def geocode_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "PythonWeatherApp/1.0"}

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200 and response.json():
        result = response.json()[0]
        return {"lat": float(result["lat"]), "lon": float(result["lon"])}

    return None

# Translate weather symbol code to readable description
def translate_symbol(symbol_code: str) -> str:
    if not symbol_code:
        return "No data"

    symbol_map = {
        "clearsky": "Clear sky",
        "clearsky_day": "Clear sky",
        "clearsky_night": "Clear sky",
        "partlycloudy_day": "Partly cloudy",
        "partlycloudy_night": "Partly cloudy",
        "cloudy": "Cloudy",
        "fair_day": "Fair weather",
        "fair_night": "Fair weather",
        "rain": "Rain",
        "lightrain": "Light rain",
        "heavyrain": "Heavy rain",
        "rainshowers": "Rain showers",
        "rainshowersandthunder": "Rain showers and thunder",
        "heavyrainandthunder": "Heavy rain with thunder",
        "sleet": "Sleet",
        "lightsleet": "Light sleet",
        "snow": "Snow",
        "lightsnow": "Light snow",
        "heavysnow": "Heavy snow",
        "fog": "Fog",
        "unknown": "No data"
    }

    if symbol_code in symbol_map:
        return symbol_map[symbol_code]

    lower = symbol_code.lower()
    if "clearsky" in lower:
        return "Clear sky"
    if "sleet" in lower:
        return "Sleet"
    if "snow" in lower:
        return "Snow"
    if "rain" in lower and "thunder" in lower:
        return "Rain with thunder"
    if "rain" in lower:
        return "Rain"
    if "cloud" in lower:
        return "Cloudy"
    if "fog" in lower:
        return "Fog"

    return symbol_code

# Fetch weather data for a given city
def get_weather(city_name):
    info = geocode_city(city_name)
    if not info:
        print("City not found. Please try again.")
        return

    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={info['lat']}&lon={info['lon']}"
    headers = {"User-Agent": "PythonWeatherApp/1.0"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch weather data.")
        return

    data = response.json()
    timeseries = data.get('properties', {}).get('timeseries', [])
    if not timeseries:
        print("No weather data available.")
        return

    # Format numeric values
    def fmt(val, unit=""):
        if isinstance(val, (int, float)):
            return f"{val:.1f}{unit}"
        if val is None:
            return "No data"
        return f"{val}{unit}"

    # Color temperature output for terminal
    def color_temp(val, unit="°C", width=6):
        base = fmt(val, unit)
        try:
            is_num = isinstance(val, (int, float))
        except Exception:
            is_num = False
        if not is_num:
            return base.rjust(width)
        if val < 0:
            color = "34"
        elif val > 0:
            color = "31"
        else:
            color = "33"
        return f"\033[{color}m{base.rjust(width)}\033[0m"

    ts0 = timeseries[0]
    time0 = ts0['time'].replace('Z', '+00:00')
    dt0 = datetime.fromisoformat(time0)
    if dt0.tzinfo is None:
        dt0 = dt0.replace(tzinfo=timezone.utc)
    local_time0 = dt0.astimezone().strftime('%Y-%m-%d %H:%M')

    inst0 = ts0['data'].get('instant', {}).get('details', {})
    temp0 = inst0.get('air_temperature')
    wind0 = inst0.get('wind_speed')
    desc0_raw = ts0['data'].get('next_1_hours', {}).get('summary', {}).get('symbol_code')
    desc0 = translate_symbol(desc0_raw) if desc0_raw else 'No data'

    print("\n" + "="*56)
    print(f"Weather for: {city_name}    (Time: {local_time0})")
    print("-"*56)
    print(f"Current: {color_temp(temp0):>10}  Wind: {fmt(wind0,' m/s'):>10}  {desc0}")
    print("-"*56)

    # Forecast for next 10 hours
    print("\nWeather forecast for the next 10 hours:")
    print(f"{'Time':19} {'Temp':>6}   {'Wind':>6}   {'Description'}")
    print("-"*56)
    n = min(10, len(timeseries))
    for i in range(n):
        ts = timeseries[i]
        tstr = ts['time'].replace('Z', '+00:00')
        dt = datetime.fromisoformat(tstr)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        time_local = dt.astimezone().strftime('%Y-%m-%d %H:%M')

        inst = ts['data'].get('instant', {}).get('details', {})
        temp = inst.get('air_temperature')
        wind = inst.get('wind_speed')
        desc_raw = ts['data'].get('next_1_hours', {}).get('summary', {}).get('symbol_code')
        desc = translate_symbol(desc_raw) if desc_raw else 'No data'

        print(f"{time_local:19} {color_temp(temp):>6}   {fmt(wind,' m/s'):>6}   {desc}")
    print("="*56 + "\n")

# Console menu
def menu():
    while True:
        print("=== Check the Weather ===")
        print("Enter city name manually or 'exit' to quit.")
        choice = input("Enter city: ").strip()

        if choice.lower() == 'exit':
            print("Goodbye!")
            break

        get_weather(choice)

# Program entry point
if __name__ == "__main__":
    menu()
