import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import polars as pl
    import matplotlib.pyplot as plt
    from pathlib import Path

    return (Path,)


@app.cell
def _(Path):

    # Set up the database file locations
    project_folder = Path("projects/db")

    data_folder = project_folder / "data"
    database = project_folder / "database.duckdb"

    print("Database:", database)
    print("Data folder:", data_folder)
    return


if __name__ == "__main__":
    app.run()
