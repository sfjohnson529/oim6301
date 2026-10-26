import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
    1. The Question
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    The student run club at Babson needs to determine which day will have the best weather for an outdoor event. This tool will use weather forecast data to compare temperatures of the day, chance of rain, and wind speeds over the next 7 days. This tool will help the club choose the best day for the event to be outside.
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    2. My Plan Before AI
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    I would find the coordinates of the Massachusetts towns that were plugged in by the viewer, then I would want to see a seven day weather forecast from Open-Meteo and gather the high and low temp chance of rain for each day. I would then select the day with the lowest chance of rain or if none of them is the obvious pick I would choose the day that seems to have the best possibilities. Lastly, I want it to layout a table of all days and what day is the recommended day to choose. 
    1. I will need a function that finds town coordinates and a function that finds the daily weather records. 
    2. they will request the open meteo address that was provided.
    3. I will make sure that the forecast has seven different dates and seven numbers for each measurement for weather. 
    4. I will count the seven dates and the seven filled out daily records and make sure that they are the same.
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    3. Inputs
    """,
    name="_"
)


@app.cell
def _():
    place = "Wellesley"
    state = "Massachusetts"
    lowest_high_f = 55
    highest_high_f = 80
    max_rain_chance = 30
    max_wind_mph = 15
    return (
        highest_high_f,
        lowest_high_f,
        max_rain_chance,
        max_wind_mph,
        place,
        state,
    )


app._unparsable_cell(
    r"""
    4. The Work
    """,
    name="_"
)


@app.cell
def _():
    import requests 

    return (requests,)


@app.cell
def _(requests):
    def get_coordinates(place, state):
        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": place,
            "count": 100,
            "countryCode": "US"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        for _location in data.get("results", []):
            if _location.get("admin1") == state:
                return {
                    "name": _location["name"],
                    "latitude": _location["latitude"],
                    "longitude": _location["longitude"]
                }

        raise ValueError("No matching town found in that state.")

    return (get_coordinates,)


@app.cell
def _(get_coordinates, place, state):
    coordinates = get_coordinates(place, state)
    print(coordinates)
    return (coordinates,)


app._unparsable_cell(
    r"""
    Forecast Function:
    """,
    name="_"
)


@app.cell
def _(requests):

    def get_forecast(latitude, longitude):
        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
            "temperature_unit": "fahrenheit",
            "wind_speed_unit": "mph",
            "timezone": "America/New_York",
            "forecast_days": 7
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        daily = data["daily"]
        forecast = []

        for _i in range(len(daily["time"])):
            _day = {
                "date": daily["time"][_i],
                "high": daily["temperature_2m_max"][_i],
                "low": daily["temperature_2m_min"][_i],
                "rain": daily["precipitation_probability_max"][_i],
                "wind": daily["wind_speed_10m_max"][_i]
            }

            forecast.append(_day)

        return forecast

    return (get_forecast,)


@app.cell
def _(coordinates, get_forecast):
    forecast = get_forecast(
        coordinates["latitude"],
        coordinates["longitude"]
    )

    for _day in forecast:
        print(_day)
    return (forecast,)


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    for _day in forecast:
        _day["passes"] = (
            lowest_high_f <= _day["high"] <= highest_high_f
            and _day["rain"] <= max_rain_chance
            and _day["wind"] <= max_wind_mph
        )

        print(_day["date"], _day["passes"])
    return


@app.cell
def _(forecast, highest_high_f, lowest_high_f, max_rain_chance, max_wind_mph):
    passing_days = []

    for _day in forecast:
        if _day["passes"]:
            passing_days.append(_day)

    if passing_days:
        best_day = min(
            passing_days,
            key=lambda _day: (_day["rain"], _day["wind"])
        )
    else:
        best_day = min(
            forecast,
            key=lambda _day: (
                int(_day["high"] < lowest_high_f)
                + int(_day["high"] > highest_high_f)
                + int(_day["rain"] > max_rain_chance)
                + int(_day["wind"] > max_wind_mph),
                _day["date"]
            )
        )

    print("Best day:", best_day["date"])
    return


if __name__ == "__main__":
    app.run()
