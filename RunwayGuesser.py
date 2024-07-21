from bs4 import BeautifulSoup
import requests

URL = "https://metar-taf.com/pl/EPKK"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}


def get_runway_number():
    wind_direction = get_wind_direction()
    if wind_direction > 348 or (wind_direction >= 0 and wind_direction < 168):
        runway_number = 7
    elif wind_direction > 168 and wind_direction < 348:
        runway_number = 25
    else:
        runway_number = -1
    return runway_number


def get_wind_direction():
    response = requests.get(URL, headers=HEADERS)
    if response.status_code == 200:
        # Parse the content of the webpage
        soup = BeautifulSoup(response.content, "html.parser")

        wind_gadget = soup.find("div", class_="my-auto py-2")

        if wind_gadget:
            unformatted_wind = (wind_gadget.text).strip()
            wind_direction = int(unformatted_wind[: len(unformatted_wind) - 1])
            return wind_direction


if __name__ == "__main__":
    print(get_wind_direction())
