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


if __name__ == "__main__":
    app.run()
