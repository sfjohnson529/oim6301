import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Reading it Back


    Question: What is the total value of assets purchased by each member across all of their portfolios?

    Prediction: I predict that the join between members, portfolios, and trades to produce about 350 rows before grouping plus any rows representing members without portfolios or portfolios without trades. Each trade should appear once because it will belong to one portfolio and each portfolio belongs to one member. I will compare this prediction with the actual row count after running the query.
    """)
    return


@app.cell
def _(mo):
    import duckdb

    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _(ask):
    ask("SELECT COUNT(*) AS total_trades FROM trades")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 1: For each portfolio over the last 30 days: the number of trades, the money spent on buys with fees added, and the money received from sells with fees taken off.
    """)
    return


@app.cell
def _():
    as_of = "2026-10-31"
    return (as_of,)


@app.cell
def _(ask):
    ask("DESCRIBE trades")
    return


@app.cell
def _(as_of, ask):
    ask(f"""
    SELECT
        portfolio_id,
        COUNT(*) AS number_of_trades,
        ROUND(SUM(
            CASE
                WHEN trade_type = 'buy'
                THEN quantity * price_per_unit + fee
                ELSE 0
            END
        ), 2) AS money_spent_on_buys,
        ROUND(SUM(
            CASE
                WHEN trade_type = 'sell'
                THEN quantity * price_per_unit - fee
                ELSE 0
            END
        ), 2) AS money_received_from_sells
    FROM trades
    WHERE trade_date BETWEEN
        DATE '{as_of}' - INTERVAL 29 DAYS
        AND DATE '{as_of}'
    GROUP BY portfolio_id
    ORDER BY portfolio_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    During the 30 day period that ends October 31st, 2026, 17 portfolios made trades. Portfolio 7 spent $552,799.61 on purchases, including fees and portfolio 10 spent $394,399.28 on purchases and received $227,574.75 from sales after fees. These results show that trading activity and transaction values varied a lot across portfolios.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 2: One row for each member, members with no portfolio included: their number of portfolios and the total value they bought across them. (three tables or more)
    """)
    return


@app.cell
def _(ask):
    ask("DESCRIBE members")
    return


@app.cell
def _(ask):
    ask("DESCRIBE portfolios")
    return


@app.cell
def _(ask):
    ask("""
    SELECT
        m.member_id,
        m.first_name,
        m.last_name,
        COUNT(DISTINCT p.portfolio_id) AS number_of_portfolios,
        ROUND(
            COALESCE(
                SUM(
                    CASE
                        WHEN t.trade_type = 'buy'
                        THEN t.quantity * t.price_per_unit
                        ELSE 0
                    END
                ), 0
            ), 2
        ) AS total_value_bought
    FROM members AS m
    LEFT JOIN portfolios AS p
        ON m.member_id = p.member_id
    LEFT JOIN trades AS t
        ON p.portfolio_id = t.portfolio_id
    GROUP BY
        m.member_id,
        m.first_name,
        m.last_name
    ORDER BY m.member_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The database contains 15 members including those without portfolios. Noah Wilson owns two portfolios and has the highest purchase value among all the members with a total of $3,264,334.43. Alex Smith also owns two portfolios with total purchases being equal to $2,619,612.05. These total values bought show the value of purchases before fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 3: What each portfolio holds on your as_of date: for each asset, the units bought minus the units sold, keeping only those above zero. (three tables or more)
    """)
    return


@app.cell
def _(ask):
    ask("DESCRIBE assets")
    return


@app.cell
def _(as_of, ask):
    ask(f"""
    SELECT
        p.portfolio_id,
        p.portfolio_name,
        a.current_ticker,
        a.asset_name,
        SUM(
            CASE
                WHEN t.trade_type = 'buy' THEN t.quantity
                WHEN t.trade_type = 'sell' THEN -t.quantity
                ELSE 0
            END
        ) AS units_held
    FROM portfolios AS p
    JOIN trades AS t
        ON p.portfolio_id = t.portfolio_id
    JOIN assets AS a
        ON t.asset_id = a.asset_id
    WHERE t.trade_date <= DATE '{as_of}'
    GROUP BY
        p.portfolio_id,
        p.portfolio_name,
        a.asset_id,
        a.current_ticker,
        a.asset_name
    HAVING SUM(
        CASE
            WHEN t.trade_type = 'buy' THEN t.quantity
            WHEN t.trade_type = 'sell' THEN -t.quantity
            ELSE 0
        END
    ) > 0
    ORDER BY p.portfolio_id, a.current_ticker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As of October 31st, 2026, the database shows 153 portfolio-asset holdings with positive balances. An example is the growth portfolio so portfolio 1, holds 24 units of Microsoft, 17 units of Bitcoin, 14 units of Ethereum, 4 units of Apple and a bunch more. These holdings represent the total units purchased minus the total units sold through the reference date of October 31st, 2026.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 4: For every trade in the last 90 days, the closing price on the trade date, and how far the trade price was from it, as a percent of the closing price. (three tables or more)
    """)
    return


@app.cell
def _(ask):
    ask("DESCRIBE closing_prices")
    return


@app.cell
def _(as_of, ask):
    ask(f"""
    SELECT
        t.trade_id,
        t.trade_date,
        a.current_ticker,
        t.trade_type,
        ROUND(t.price_per_unit, 2) AS trade_price,
        ROUND(cp.closing_price, 2) AS closing_price,
        ROUND(
            (t.price_per_unit - cp.closing_price)
            / cp.closing_price * 100,
            2
        ) AS percentage_difference
    FROM trades AS t
    JOIN assets AS a
        ON t.asset_id = a.asset_id
    LEFT JOIN closing_prices AS cp
        ON t.asset_id = cp.asset_id
        AND t.trade_date = cp.price_date
    WHERE t.trade_date BETWEEN
        DATE '{as_of}' - INTERVAL 89 DAYS
        AND DATE '{as_of}'
    ORDER BY t.trade_date DESC, t.trade_id
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the last 90 days, there were 164 trades. For example, Bitcoin was purchased on October 31st, at $78,442.03 compared to a closing price of %79,010.75 this represents a 0.72% discount to the closing price. One October 30th, Apple was purchased at $195.40 which is about a 95% discount below its closing price of $197.27.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 5: The assets the club follows that no portfolio has ever traded.
    """)
    return


@app.cell
def _(ask):
    ask("""
    SELECT
        a.asset_id,
        a.current_ticker,
        a.asset_name
    FROM assets AS a
    LEFT JOIN trades AS t
        ON a.asset_id = t.asset_id
    WHERE t.trade_id IS NULL
    ORDER BY a.current_ticker
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Solana (SOL) asset_id 15 is the only asset followed by the Babson Investment Club that has never been traded by any portfolio. All 14 other assets have at least one trade.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 6: The asset that changed its ticker: its value traded over the year, under both tickers together.
    """)
    return


@app.cell
def _(ask):
    ask("DESCRIBE ticker_history")
    return


@app.cell
def _(ask):
    ask("""
    SELECT
        a.asset_id,
        a.asset_name,
        STRING_AGG(th.ticker, ' → ' ORDER BY th.start_date) AS ticker_history,
        COUNT(*) AS number_of_tickers
    FROM assets AS a
    JOIN ticker_history AS th
        ON a.asset_id = th.asset_id
    GROUP BY a.asset_id, a.asset_name
    HAVING COUNT(*) > 1
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
    SELECT
        a.asset_id,
        a.asset_name,
        STRING_AGG(DISTINCT th.ticker, ', ') AS tickers,
        COUNT(DISTINCT t.trade_id) AS total_trades,
        ROUND(SUM(t.quantity * t.price_per_unit), 2) AS total_trading_value
    FROM assets AS a
    JOIN trades AS t
        ON a.asset_id = t.asset_id
    JOIN ticker_history AS th
        ON a.asset_id = th.asset_id
        AND t.trade_date >= th.start_date
        AND (th.end_date IS NULL OR t.trade_date <= th.end_date)
    WHERE a.asset_id = 6
        AND t.trade_date BETWEEN
            DATE '{as_of}' - INTERVAL 1 YEAR + INTERVAL 1 DAY
            AND DATE '{as_of}'
    GROUP BY a.asset_id, a.asset_name
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    META Platforms (asset ID 6) changed its ticker from METAOLD to META. During the year period that ends October 31st, the asset had 27 trades with a combined trading value of $84,144.25. This total includes purchases and sales that were made under both ticker symbols without subtracting sales or without including transaction fees.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 7: Every trade checked against the rule that it happens on a day its asset has a closing price, and a list of any that break it. (checks a rule)
    """)
    return


@app.cell
def _(ask):
    ask("""
    SELECT
        t.trade_id,
        t.portfolio_id,
        a.current_ticker,
        t.trade_date,
        t.trade_type,
        t.quantity
    FROM trades AS t
    JOIN assets AS a
        ON t.asset_id = a.asset_id
    LEFT JOIN closing_prices AS cp
        ON t.asset_id = cp.asset_id
        AND t.trade_date = cp.price_date
    WHERE cp.asset_id IS NULL
    ORDER BY t.trade_id
    """)
    return


if __name__ == "__main__":
    app.run()
