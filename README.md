## 🇵🇱 Wersja polska
# python-weather-cli
---

Proste narzędzie konsolowe napisane w Pythonie, które pobiera aktualne dane pogodowe z API MET Norway i wyświetla czytelną prognozę na 10 godzin wraz z kolorowym formatowaniem temperatury w terminalu.

🎥 [Obejrzyj na YouTube ↗](https://youtu.be/29mKGsPk6TE)

## Funkcje

- 🌍 Automatyczne geokodowanie miast (OpenStreetMap / Nominatim)
- ☀️ Aktualna pogoda z MET Norway
- 🎨 Kolorowe wyświetlanie temperatury w konsoli
- 📅 Konwersja czasu na lokalny
- 🔍 Szczegółowa prognoza na 10 godzin
- 🇵🇱 Polskie opisy pogody (tłumaczenie symboli)
- 🛠 Proste i lekkie — brak zewnętrznych zależności poza requests

## Instalacja

Sklonuj repozytorium:

```bash
git clone https://github.com/<twoje-konto>/python-weather-cli.git
cd python-weather-cli
```

Zainstaluj zależności:

```bash
pip install requests
```

## Użycie

Uruchom główny skrypt:

```bash
python main.py
```

Po uruchomieniu:

* Wpisz nazwę miasta (np. Oslo, Warszawa, London)
* Lub wpisz exit, aby zakończyć działanie programu

## Przykładowy wynik

```markdown
========================================================
Pogoda dla: Oslo    (czas: 2025-12-05 14:00)
--------------------------------------------------------
Aktualnie:    2.3°C  Wiatr:   3.1 m/s  Czyste niebo
--------------------------------------------------------

Pogoda na nastpne 10 godzin:
Godzina               Temperatura   Wiatr    Opis
--------------------------------------------------------
2025-12-05 15:00          2.1°C     3.0 m/s  Czesciowo zachmurzone
...
========================================================
```

## Licencja

Ten projekt jest udostępniany na licencji MIT.
Szczegóły znajdziesz w pliku `LICENSE`.

## Podziękowania za API

* Geokodowanie: OpenStreetMap Nominatim
* Dane pogodowe: MET Norway (api.met.no)

## Autor

* Stworzone przez Greg — PotegaIT
* YouTube: [@PotegaIT](https://www.youtube.com/@PotegaIT)

   
   
## 🇬🇧 English version
# python-weather-cli
---

A simple command-line tool written in Python that fetches real-time weather data using the MET Norway API and displays a clean 10-hour forecast with colored console output.

🎥 [Watch on YouTube ↗](https://youtu.be/29mKGsPk6TE)


## Features
- 🌍 Automatic city geocoding (OpenStreetMap / Nominatim)
- ☀️ Real-time weather from MET Norway
- 🎨 Colorized temperature output in terminal
- 📅 Local time conversion
- 🔍 10-hour detailed forecast
- 🇵🇱 Polish weather descriptions (symbol translation)
- 🛠 Simple and lightweight — no external packages except `requests`

## Installation

Clone the repository:

```bash
git clone https://github.com/<twoje-konto>/python-weather-cli.git
cd python-weather-cli
```

Install dependencies:

```bash
pip install requests
```

## Usage

Run the main script:

```bash
python main.py
```
When prompted:

* Enter the city name (e.g. Oslo, Warszawa, London)
* Or type exit to close the program


## Example Output

```markdown
========================================================
Pogoda dla: Oslo    (czas: 2025-12-05 14:00)
--------------------------------------------------------
Aktualnie:    2.3°C  Wiatr:   3.1 m/s  Czyste niebo
--------------------------------------------------------

Pogoda na nastpne 10 godzin:
Godzina               Temperatura   Wiatr    Opis
--------------------------------------------------------
2025-12-05 15:00          2.1°C     3.0 m/s  Czesciowo zachmurzone
...
========================================================
```

## License

This project is licensed under the MIT License.
See the `LICENSE` file for details.

## API Credits

* Geocoding: OpenStreetMap Nominatim
* Weather data: MET Norway (api.met.no)

## Author

Created by Greg — PotegaIT
YouTube: [@PotegaIT](https://www.youtube.com/@PotegaIT)

