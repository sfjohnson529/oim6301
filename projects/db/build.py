import marimo as mo
import duckdb
import polars as pl
import matplotlib.pyplot as plt
from pathlib import Path


# Locate the project folder
project_folder = Path(__file__).parent

# Locate the CSV data folder
data_folder = project_folder / "data"

# Choose where the database will be saved
database = project_folder / "database.duckdb"

# Remove the old database so each run starts fresh
if database.exists():
    database.unlink()

print("Database location:", database)
print("Data folder:", data_folder)

# Create the database and the members table
with duckdb.connect(str(database)) as _con:

    _con.execute("""
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

    print("Created members table")


    # Create the portfolios table
    _con.execute("""
        CREATE TABLE portfolios (
            portfolio_id INTEGER PRIMARY KEY,
            member_id INTEGER NOT NULL,
            portfolio_name VARCHAR NOT NULL,
            created_date DATE NOT NULL,
            strategy VARCHAR,

            FOREIGN KEY (member_id)
                REFERENCES members(member_id)
        )
    """)

    print("Created portfolios table")
        # Create the assets table
    _con.execute("""
        CREATE TABLE assets (
            asset_id INTEGER PRIMARY KEY,
            current_ticker VARCHAR NOT NULL UNIQUE,
            asset_name VARCHAR NOT NULL,
            asset_type VARCHAR NOT NULL,
            sector VARCHAR,

            CHECK (asset_type IN ('stock', 'ETF', 'crypto'))
        )
    """)

    print("Created assets table")
    # Create the ticker history table
    _con.execute("""
        CREATE TABLE ticker_history (
            ticker_history_id INTEGER PRIMARY KEY,
            asset_id INTEGER NOT NULL,
            ticker VARCHAR NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE,

            FOREIGN KEY (asset_id)
                REFERENCES assets(asset_id),

            CHECK (
                end_date IS NULL
                OR end_date >= start_date
            ),

            UNIQUE (asset_id, start_date)
        )
    """)
    print("Created ticker_history table")

       # Create the closing prices table
    _con.execute("""
        CREATE TABLE closing_prices (
            asset_id INTEGER NOT NULL,
            price_date DATE NOT NULL,
            closing_price DOUBLE NOT NULL,

            PRIMARY KEY (asset_id, price_date),

            FOREIGN KEY (asset_id)
                REFERENCES assets(asset_id),

            CHECK (closing_price > 0)
        )
    """)

    print("Created closing_prices table")


    # Create the trades table
    _con.execute("""
        CREATE TABLE trades (
            trade_id INTEGER PRIMARY KEY,
            portfolio_id INTEGER NOT NULL,
            asset_id INTEGER NOT NULL,
            trade_date DATE NOT NULL,
            trade_type VARCHAR NOT NULL,
            quantity INTEGER NOT NULL,
            price_per_unit DOUBLE NOT NULL,
            fee DOUBLE NOT NULL DEFAULT 0,

            FOREIGN KEY (portfolio_id)
                REFERENCES portfolios(portfolio_id),

            FOREIGN KEY (asset_id)
                REFERENCES assets(asset_id),

            CHECK (trade_type IN ('buy', 'sell')),
            CHECK (quantity > 0),
            CHECK (price_per_unit > 0),
            CHECK (fee >= 0),

            UNIQUE (portfolio_id, asset_id, trade_date)
        )
    """)

    print("Created trades table")

      # Load CSV data into the six tables
    tables = [
        "members",
        "portfolios",
        "assets",
        "ticker_history",
        "closing_prices",
        "trades"
    ]

    for table in tables:
        csv_path = data_folder / f"{table}.csv"

        _con.execute(
            f"""
            INSERT INTO {table}
            SELECT * FROM read_csv_auto(?)
            """,
            [str(csv_path)]
        )

        print(f"Loaded {table}.csv")

    # Check how many records are in each table
    print("\nDatabase Row Counts:")

    for table in tables:
        result = _con.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()

        print(f"{table}: {result[0]} rows")

    
    # A Row It Refuses
    # Try to insert a member with an existing member ID

    print("\nA Row It Refuses:")

    try:
        _con.execute("""
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

    except duckdb.ConstraintException as error:
        print("DuckDB rejected the row:")
        print(error)

#answers you already know
    print("\nAnswers You Already Knew:")

    # Check 1: There should be 15 members
    member_count = _con.execute("""
        SELECT COUNT(*) FROM members
    """).fetchone()[0]

    print("Check 1 - Members:", member_count)
    assert member_count == 15

    # Check 2: There should be 15 assets
    asset_count = _con.execute("""
        SELECT COUNT(*) FROM assets
    """).fetchone()[0]

    print("Check 2 - Assets:", asset_count)
    assert asset_count == 15

    # Check 3: There should be 354 trades
    trade_count = _con.execute("""
        SELECT COUNT(*) FROM trades
    """).fetchone()[0]

    print("Check 3 - Trades:", trade_count)
    assert trade_count == 350

    print("All three checks passed!")

    # a view
    print("\nA View:")

    _con.execute("""
        CREATE VIEW portfolio_summary AS
        SELECT
            p.portfolio_id,
            p.portfolio_name,
            m.first_name,
            m.last_name,
            COUNT(t.trade_id) AS total_trades
        FROM portfolios p
        JOIN members m
            ON p.member_id = m.member_id
        LEFT JOIN trades t
            ON p.portfolio_id = t.portfolio_id
        GROUP BY
            p.portfolio_id,
            p.portfolio_name,
            m.first_name,
            m.last_name
    """)

    # Display the first five rows of the view
    result = _con.execute("""
        SELECT *
        FROM portfolio_summary
        ORDER BY total_trades DESC
        LIMIT 5
    """).fetchdf()

    print(result)
# a look at the data
    print("\nA Look at the Data:")

    # Get trade counts for each asset
    trade_data = _con.execute("""
        SELECT
            a.current_ticker,
            COUNT(t.trade_id) AS total_trades
        FROM assets a
        LEFT JOIN trades t
            ON a.asset_id = t.asset_id
        GROUP BY a.current_ticker
        ORDER BY total_trades DESC
    """).pl()

    # Use Polars to organize the results
    trade_data = pl.DataFrame(trade_data)

    # Create a bar chart
    plt.figure(figsize=(10, 5))
    plt.bar(
        trade_data["current_ticker"].to_list(),
        trade_data["total_trades"].to_list()
    )

    plt.title("Number of Trades by Investment Asset")
    plt.xlabel("Investment Asset")
    plt.ylabel("Number of Trades")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    print(
        "This chart shows which investment assets "
        "were traded most frequently by club members."
    )

