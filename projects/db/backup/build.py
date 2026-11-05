# %%

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    import marimo as mo
    import matplotlib.pyplot as plt
    import polars as pl
    from pathlib import Path

    return Path, duckdb, mo, pl, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Babson Investment Club Database
    """)
    return


@app.cell
def _(Path):
    project_folder = Path(__file__).resolve().parents[1]
    data_folder = project_folder / "data"
    database = project_folder / "database.duckdb"

    paths = {
        "Database": str(database),
        "CSV data": str(data_folder),
    }
    paths
    return data_folder, database


@app.cell
def _(data_folder, database, duckdb):
    table_names = [
        "members",
        "portfolios",
        "assets",
        "ticker_history",
        "closing_prices",
        "trades",
    ]

    if database.exists():
        database.unlink()

    with duckdb.connect(str(database)) as build_connection:
        build_connection.execute("""
            CREATE TABLE members (
                member_id INTEGER PRIMARY KEY,
                first_name VARCHAR NOT NULL,
                last_name VARCHAR NOT NULL,
                school_email VARCHAR NOT NULL UNIQUE,
                class_year INTEGER NOT NULL,
                join_date DATE NOT NULL,
                CHECK (class_year BETWEEN 2026 AND 2029)
            )
        """)

        build_connection.execute("""
            CREATE TABLE portfolios (
                portfolio_id INTEGER PRIMARY KEY,
                member_id INTEGER NOT NULL,
                portfolio_name VARCHAR NOT NULL,
                created_date DATE NOT NULL,
                strategy VARCHAR,
                FOREIGN KEY (member_id) REFERENCES members(member_id)
            )
        """)

        build_connection.execute("""
            CREATE TABLE assets (
                asset_id INTEGER PRIMARY KEY,
                current_ticker VARCHAR NOT NULL UNIQUE,
                asset_name VARCHAR NOT NULL,
                asset_type VARCHAR NOT NULL,
                sector VARCHAR,
                CHECK (asset_type IN ('stock', 'ETF', 'crypto'))
            )
        """)

        build_connection.execute("""
            CREATE TABLE ticker_history (
                ticker_history_id INTEGER PRIMARY KEY,
                asset_id INTEGER NOT NULL,
                ticker VARCHAR NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE,
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
                CHECK (end_date IS NULL OR end_date >= start_date),
                UNIQUE (asset_id, start_date)
            )
        """)

        build_connection.execute("""
            CREATE TABLE closing_prices (
                asset_id INTEGER NOT NULL,
                price_date DATE NOT NULL,
                closing_price DOUBLE NOT NULL,
                PRIMARY KEY (asset_id, price_date),
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
                CHECK (closing_price > 0)
            )
        """)

        build_connection.execute("""
            CREATE TABLE trades (
                trade_id INTEGER PRIMARY KEY,
                portfolio_id INTEGER NOT NULL,
                asset_id INTEGER NOT NULL,
                trade_date DATE NOT NULL,
                trade_type VARCHAR NOT NULL,
                quantity INTEGER NOT NULL,
                price_per_unit DOUBLE NOT NULL,
                fee DOUBLE NOT NULL DEFAULT 0,
                FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id),
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
                CHECK (trade_type IN ('buy', 'sell')),
                CHECK (quantity > 0),
                CHECK (price_per_unit > 0),
                CHECK (fee >= 0),
                UNIQUE (portfolio_id, asset_id, trade_date)
            )
        """)

        for table_name in table_names:
            csv_path = data_folder / f"{table_name}.csv"
            build_connection.execute(
                f"INSERT INTO {table_name} SELECT * FROM read_csv_auto(?)",
                [str(csv_path)],
            )

        build_connection.execute("""
            CREATE VIEW portfolio_summary AS
            SELECT
                p.portfolio_id,
                p.portfolio_name,
                m.first_name,
                m.last_name,
                COUNT(t.trade_id) AS total_trades
            FROM portfolios p
            JOIN members m ON p.member_id = m.member_id
            LEFT JOIN trades t ON p.portfolio_id = t.portfolio_id
            GROUP BY
                p.portfolio_id,
                p.portfolio_name,
                m.first_name,
                m.last_name
        """)

    database_ready = True
    return (table_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Table row counts
    """)
    return


@app.cell
def _(database, duckdb, pl, table_names):
    with duckdb.connect(str(database), read_only=True) as count_connection:
        row_counts = [
            {
                "table": table_name,
                "rows": count_connection.execute(
                    f"SELECT COUNT(*) FROM {table_name}"
                ).fetchone()[0],
            }
            for table_name in table_names
        ]

    counts_df = pl.DataFrame(row_counts)
    counts_df
    return (counts_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Checks and constraints
    """)
    return


@app.cell
def _(counts_df, mo):
    expected_counts = {
        "members": 15,
        "assets": 15,
        "trades": 350,
    }
    actual_counts = dict(zip(counts_df["table"], counts_df["rows"]))
    checks_passed = all(
        actual_counts[table_name] == expected_count
        for table_name, expected_count in expected_counts.items()
    )
    assert checks_passed, f"Unexpected row counts: {actual_counts}"
    mo.md("All expected row-count checks passed.")
    return


@app.cell
def _(database, duckdb, mo):
    with duckdb.connect(str(database)) as constraint_connection:
        try:
            constraint_connection.execute("""
                INSERT INTO members (
                    member_id,
                    first_name,
                    last_name,
                    school_email,
                    class_year,
                    join_date
                )
                VALUES (
                    1,
                    'Test',
                    'Student',
                    'teststudent@babson.edu',
                    2027,
                    '2026-09-01'
                )
            """)
            rejected_row = "The duplicate row was unexpectedly accepted."
        except duckdb.ConstraintException as error:
            rejected_row = f"DuckDB rejected the duplicate member ID: {error}"

    mo.md(f"**A row it refuses:** {rejected_row}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Portfolio summary view
    """)
    return


@app.cell
def _(database, duckdb, pl):
    with duckdb.connect(str(database), read_only=True) as preview_connection:
        portfolio_preview = preview_connection.execute("""
            SELECT *
            FROM portfolio_summary
            ORDER BY total_trades DESC
            LIMIT 5
        """).pl()

    pl.DataFrame(portfolio_preview)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Trades by asset
    """)
    return


@app.cell
def _(database, duckdb, plt):
    with duckdb.connect(str(database), read_only=True) as chart_connection:
        trade_data = chart_connection.execute("""
            SELECT
                a.current_ticker,
                COUNT(t.trade_id) AS total_trades
            FROM assets a
            LEFT JOIN trades t ON a.asset_id = t.asset_id
            GROUP BY a.current_ticker
            ORDER BY total_trades DESC
        """).pl()

    figure, axes = plt.subplots(figsize=(10, 5))
    axes.bar(
        trade_data["current_ticker"].to_list(),
        trade_data["total_trades"].to_list(),
    )
    axes.set_title("Number of Trades by Investment Asset")
    axes.set_xlabel("Investment Asset")
    axes.set_ylabel("Number of Trades")
    axes.tick_params(axis="x", labelrotation=45)
    figure.tight_layout()
    figure
    return


if __name__ == "__main__":
    app.run()
