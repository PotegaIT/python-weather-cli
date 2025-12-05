import requests 
from datetime import datetime, timezone 
 
# Pobiera wspolrzedne geograficzne dla podanego miasta 
# Fetches geographic coordinates for a given city
def geocode_city(city_name): 
    # API OpenStreetMap do wyszukiwania miejsc 
    # OpenStreetMap API for searching locations
    url = "https://nominatim.openstreetmap.org/search" 
    # parametry zapytania 
    # request parameters
    params = { 
        # nazwa miasta, ktore chcemy znalezc 
        # name of the city to find
        "q": city_name, 
        # chcemy dostac dane w formacie JSON 
        # we want data in JSON format
        "format": "json", 
        # pobieramy tylko pierwszy wynik 
        # retrieve only the first result
        "limit": 1 
    } 
    # API wymaga podania "User-Agent" 
    # API requires a "User-Agent"
    headers = {"User-Agent": "PythonWeatherApp/1.0"} 
 
    # wysylamy zapytanie GET i zapisujemy odpowiedz 
    # send GET request and store the response
    response = requests.get(url, params=params, headers=headers) 
 
    # odpowiedz jest poprawna i mamy jakies dane: 
    # if the response is valid and contains data
    if response.status_code == 200 and response.json(): 
        # bierzemy pierwszy wynik 
        # take the first result
        result = response.json()[0] 
        # zwracamy wspolrzedne jako liczby zmiennoprzecinkowe 
        # return coordinates as float numbers
        return {"lat": float(result["lat"]), "lon": float(result["lon"])} 
 
    # nie udalo sie znalezc miasta 
    # failed to find city
    return None 
 
# tlumaczenie symbolu pogodowego 
# weather symbol translation
def translate_symbol(symbol_code: str) -> str: 
    # jesli symbol jest pusty 
    # if the symbol is empty
    if not symbol_code: 
        return "brak danych" 
        # no data
 
    # mapa najczestszych symboli na polski opis 
    # map of common symbols to Polish description
    symbol_map = { 
        "clearsky": "Czyste niebo", 
        "clearsky_day": "Czyste niebo", 
        "clearsky_night": "Czyste niebo", 
        "partlycloudy_day": "Czesciowo zachmurzone", 
        "partlycloudy_night": "Czesciowo zachmurzone", 
        "cloudy": "Pochmurno", 
        "fair_day": "Ladna pogoda", 
        "fair_night": "Ladna pogoda", 
        "rain": "Deszcz", 
        "lightrain": "Lekki deszcz", 
        "heavyrain": "Ulewny deszcz", 
        "rainshowers": "Przelotne opady deszczu", 
        "rainshowersandthunder": "Przelotne opady i burze", 
        "heavyrainandthunder": "Ulewny deszcz z burza", 
        "sleet": "Deszcz ze sniegiem", 
        "lightsleet": "Lekki deszcz ze sniegiem", 
        "snow": "Snieg", 
        "lightsnow": "Lekki snieg", 
        "heavysnow": "Silne opady sniegu", 
        "fog": "Mgla", 
        "unknown": "Brak danych" 
    } 
  
    # symbol znajduje sie w mapie 
    # symbol exists in the map
    if symbol_code in symbol_map:   
        return symbol_map[symbol_code] 
 
    # symbol jest troche inny   sprawdzamy czesciowo 
    # symbol is slightly different — check partially
    lower = symbol_code.lower() 
    if "clearsky" in lower: 
        return "Czyste niebo" 
        # Clear sky
    if "sleet" in lower: 
        return "Deszcz ze sniegiem" 
        # Sleet
    if "snow" in lower: 
        return "Snieg"  
        # Snow
    if "rain" in lower and "thunder" in lower: 
        return "Deszcz z burza" 
        # Rain with thunder
    if "rain" in lower: 
        return "Deszcz" 
        # Rain
    if "cloud" in lower: 
        return "Zachmurzenie" 
        # Cloudy
    if "fog" in lower: 
        return "Mgla"  
        # Fog
 
    # nie pasuje nic  zostawiamy oryginalny kod 
    # nothing matches, return original code
    return symbol_code 
 
# pobieranie pogody 
# fetch weather data
def get_weather(city_name): 
    # geokodujemy miasto 
    # geocode the city
    info = geocode_city(city_name) 
    # brak wspolrzednych 
    # coordinates not found
    if not info: 
        print("Nie znaleziono miasta. Sprobuj ponownie.") 
        # City not found. Try again.
        return 
   
    # tworzymy URL do API pogody 
    # create URL for weather API
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={info['lat']}&lon={info['lon']}" 
    headers = {"User-Agent": "PythonWeatherApp/1.0"} 
 
    # pobieramy dane z API 
    # fetch data from API
    response = requests.get(url, headers=headers) 
    if response.status_code != 200: 
        print("Nie udalo sie pobrac danych.") 
        # Failed to fetch data
        return 
 
    # zamieniamy JSON na slownik 
    # convert JSON to dictionary
    data = response.json() 
    timeseries = data.get('properties', {}).get('timeseries', []) 
    if not timeseries: 
        print("Brak danych pogodowych.") 
        # No weather data available
        return 
 
    # formatowanie wartosci numerycznych 
    # formatting numeric values
    def fmt(val, unit=""): 
        if isinstance(val, (int, float)): 
            # zaokraglamy do 1 miejsca po przecinku 
            # round to 1 decimal
            return f"{val:.1f}{unit}" 
        if val is None: 
            return "brak danych" 
            # no data
        return f"{val}{unit}" 
     
    # kolorowanie temperatury w konsoli 
    # color temperature output in terminal
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
 
    # aktualny czas 
    # current time
    ts0 = timeseries[0] 
    # zamiana Z na +00:00 
    # replace Z with +00:00
    time0 = ts0['time'].replace('Z', '+00:00') 
    dt0 = datetime.fromisoformat(time0) 
    if dt0.tzinfo is None: 
        dt0 = dt0.replace(tzinfo=timezone.utc) 
    # lokalna godzina 
    # local time
    local_time0 = dt0.astimezone().strftime('%Y-%m-%d %H:%M') 
 
    inst0 = ts0['data'].get('instant', {}).get('details', {}) 
    temp0 = inst0.get('air_temperature') 
    wind0 = inst0.get('wind_speed') 
    desc0_raw = ts0['data'].get('next_1_hours', {}).get('summary', {}).get('symbol_code') 
    desc0 = translate_symbol(desc0_raw) if desc0_raw else 'brak danych' 
 
    print("\n" + "="*56) 
    print(f"Pogoda dla: {city_name}    (czas: {local_time0})") 
    # Weather for city (time)
    print("-"*56) 
    print(f"Aktualnie: {color_temp(temp0):>10}  Wiatr: {fmt(wind0,' m/s'):>10}  {desc0}") 
    # Current: temp, wind, description
    print("-"*56) 
 
    # prognoza na kolejne 10 godzin 
    # forecast for next 10 hours
    print("\nPogoda na nastpne 10 godzin:") 
    print(f"{'Godzina':19} {'Temperatura':>6}   {'Wiatr':>6}   {'Opis'}") 
    # Hour, Temp, Wind, Description
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
        desc = translate_symbol(desc_raw) if desc_raw else 'brak danych' 
 
        print(f"{time_local:19} {color_temp(temp):>6}   {fmt(wind,' m/s'):>6}   {desc}") 
    print("="*56 + "\n") 
 
# menu w konsoli 
# console menu
def menu(): 
    while True: 
        print("=== Sprawdz pogode ===") 
        # Check the weather
        print("Wpisz nazwe miasta recznie lub 'exit', aby zakonczyc.") 
        # Enter the city name manually or 'exit' to quit
        choice = input("Podaj miasto: ").strip() 
        # Enter city

        if choice.lower() == 'exit': 
            print("Do widzenia!") 
            # Goodbye
            break 
 
        get_weather(choice) 
 
# start programu 
# program entry point
if __name__ == "__main__": 
    menu()
