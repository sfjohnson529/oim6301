from pathlib import Path
import csv
import random
from datetime import date, timedelta

random.seed(1234)

data_folder = Path(__file__).parent / "data"
data_folder.mkdir(parents=True, exist_ok=True)

as_of = date(2026, 10, 31)
start_date = date(2025, 11, 1)
print("Data folder is ready!")
print("As-of date:", as_of)

# Generate 15 investment club members
first_names = [
    "Alex", "Emma", "James", "Olivia", "Noah",
    "Sophia", "Liam", "Ava", "Ethan", "Mia",
    "Lucas", "Isabella", "Jack", "Grace", "Ben"
]

last_names = [
    "Smith", "Johnson", "Brown", "Davis", "Wilson",
    "Taylor", "Anderson", "Thomas", "Moore", "Martin",
    "White", "Harris", "Clark", "Lewis", "Walker"
]

members = []

for i in range(15):
    join_date = as_of - timedelta(days=random.randint(30, 365))

    members.append({
        "member_id": i + 1,
        "first_name": first_names[i],
        "last_name": last_names[i],
        "school_email": f"member{i+1}@babson.edu",
        "class_year": random.randint(2026, 2029),
        "join_date": join_date.isoformat()
    })

with open(data_folder / "members.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=members[0].keys())
    writer.writeheader()
    writer.writerows(members)

print("Created members.csv with", len(members), "members")

# Generate investment portfolios
portfolios = []

portfolio_names = [
    "Growth Portfolio",
    "Value Portfolio",
    "Technology Portfolio",
    "Dividend Portfolio",
    "Balanced Portfolio",
    "Index Fund Portfolio",
    "Crypto Portfolio",
    "Long-Term Portfolio",
    "Income Portfolio",
    "Aggressive Portfolio",
    "Conservative Portfolio",
    "ESG Portfolio",
    "Retirement Portfolio",
    "Blue Chip Portfolio",
    "Momentum Portfolio",
    "Global Portfolio",
    "Small Cap Portfolio",
    "ETF Portfolio"
]

strategies = [
    "Growth", "Value", "Income",
    "Balanced", "Aggressive", "Conservative"
]

for i in range(18):
    member_id = (i % 12) + 1

    portfolios.append({
        "portfolio_id": i + 1,
        "member_id": member_id,
        "portfolio_name": portfolio_names[i],
        "created_date": (
            as_of - timedelta(days=random.randint(1, 300))
        ).isoformat(),
        "strategy": random.choice(strategies + [None])
    })

with open(data_folder / "portfolios.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=portfolios[0].keys())
    writer.writeheader()
    writer.writerows(portfolios)

print("Created portfolios.csv with", len(portfolios), "portfolios")

# Generate 15 assets: stocks, ETFs, and cryptocurrencies
assets = [
    (1, "AAPL", "Apple", "stock", "Technology"),
    (2, "MSFT", "Microsoft", "stock", "Technology"),
    (3, "NVDA", "NVIDIA", "stock", "Technology"),
    (4, "AMZN", "Amazon", "stock", "Consumer Discretionary"),
    (5, "GOOGL", "Alphabet", "stock", "Communication Services"),
    (6, "META", "Meta Platforms", "stock", "Communication Services"),
    (7, "TSLA", "Tesla", "stock", "Consumer Discretionary"),
    (8, "JPM", "JPMorgan Chase", "stock", "Financials"),
    (9, "SPY", "SPDR S&P 500 ETF", "ETF", "Broad Market"),
    (10, "QQQ", "Invesco QQQ ETF", "ETF", "Technology"),
    (11, "VTI", "Vanguard Total Stock Market ETF", "ETF", "Broad Market"),
    (12, "BND", "Vanguard Total Bond Market ETF", "ETF", "Fixed Income"),
    (13, "BTC", "Bitcoin", "crypto", None),
    (14, "ETH", "Ethereum", "crypto", None),
    (15, "SOL", "Solana", "crypto", None)
]

with open(data_folder / "assets.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "asset_id", "current_ticker",
        "asset_name", "asset_type", "sector"
    ])
    writer.writerows(assets)

print("Created assets.csv with", len(assets), "assets")

# Generate ticker history for all 15 assets
ticker_history = []

for asset in assets:
    asset_id = asset[0]
    ticker = asset[1]

    if asset_id == 6:
        # Fictional ticker change for Meta Platforms
        ticker_history.append([
            6, asset_id, "METAOLD",
            "2025-11-01", "2026-05-31"
        ])
        ticker_history.append([
            16, asset_id, "META",
            "2026-06-01", ""
        ])
    else:
        ticker_history.append([
            asset_id, asset_id, ticker,
            "2025-11-01", ""
        ])

with open(data_folder / "ticker_history.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "ticker_history_id", "asset_id",
        "ticker", "start_date", "end_date"
    ])
    writer.writerows(ticker_history)

print(
    "Created ticker_history.csv with",
    len(ticker_history), "records"
)

#closing prices
starting_prices = {
    1: 200, 2: 420, 3: 140, 4: 210, 5: 180,
    6: 600, 7: 250, 8: 230, 9: 580, 10: 500,
    11: 300, 12: 75, 13: 95000, 14: 3000, 15: 180
}

closing_prices = []
current_date = start_date

while current_date <= as_of:
    for asset in assets:
        asset_id = asset[0]
        asset_type = asset[3]

        # Stocks and ETFs have no weekend closing prices
        if asset_type != "crypto" and current_date.weekday() >= 5:
            continue

        old_price = starting_prices[asset_id]
        daily_change = random.uniform(-0.03, 0.03)
        new_price = round(old_price * (1 + daily_change), 2)

        starting_prices[asset_id] = new_price

        closing_prices.append({
            "asset_id": asset_id,
            "price_date": current_date.isoformat(),
            "closing_price": new_price
        })

    current_date += timedelta(days=1)

with open(data_folder / "closing_prices.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "asset_id", "price_date", "closing_price"
        ]
    )
    writer.writeheader()
    writer.writerows(closing_prices)

print(
    "Created closing_prices.csv with",
    len(closing_prices), "records"
)

trades = []
holdings = {}

price_lookup = {
    (p["asset_id"], p["price_date"]): p["closing_price"]
    for p in closing_prices
}

# Asset 15 is intentionally never traded
trade_assets = list(range(1, 15))

possible_trades = []

for portfolio in portfolios:
    portfolio_id = portfolio["portfolio_id"]
    created_date = portfolio["created_date"]

    for asset_id in trade_assets:
        for asset_date, price in [
            (p["price_date"], p["closing_price"])
            for p in closing_prices
            if p["asset_id"] == asset_id
        ]:
            if asset_date >= created_date:
                possible_trades.append(
                    (asset_date, portfolio_id, asset_id)
                )

random.shuffle(possible_trades)
selected_trades = sorted(possible_trades[:350])

# Generate 350 valid trades
for trade_date, portfolio_id, asset_id in selected_trades:
    key = (portfolio_id, asset_id)
    owned = holdings.get(key, 0)

    if owned == 0 or random.random() < 0.7:
        trade_type = "buy"
        quantity = random.randint(1, 10)
        holdings[key] = owned + quantity
    else:
        trade_type = "sell"
        quantity = random.randint(1, owned)
        holdings[key] = owned - quantity

    closing_price = price_lookup[(asset_id, trade_date)]
    price_per_unit = round(
        closing_price * random.uniform(0.99, 1.01), 2
    )

    trades.append({
        "trade_id": len(trades) + 1,
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "trade_date": trade_date,
        "trade_type": trade_type,
        "quantity": quantity,
        "price_per_unit": price_per_unit,
        "fee": random.choice([0, 0, 0, 1.00, 2.50])
    })
with open(data_folder / "trades.csv", "w", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "trade_id", "portfolio_id", "asset_id",
            "trade_date", "trade_type", "quantity",
            "price_per_unit", "fee"
        ]
    )
    writer.writeheader()
    writer.writerows(trades)

print("Created trades.csv with", len(trades), "trades")