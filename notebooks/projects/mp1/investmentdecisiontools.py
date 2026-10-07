# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


app._unparsable_cell(
    r"""
    This investment tool would be useful for people who are deciding where to invest their money and want to compare different investment options. With this tool, they could see how different rates of return and monthly contributions could affect the value of their investment over time which would make it easier to choose the option that would provide the best outcome for their own financial goals. It would be best for people who don't know much about investing, and are just starting out. 
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


app._unparsable_cell(
    r"""
    How I would solve this problem: I would start with the amount of money that I would initially invest (20,000) and the amount that I plan to add each month (500). Then I would add the expected annual return for each investment option. Convert the annual return into a monthly return, and then go through each month throughout the year and calculate how much the investment grows, remembering to add the monthly contribution to the investment after calculating the growth and keep doing this until I reach the number of months I entered (60 months or 5 years). Finally I would find the ending value for each option and compare the results. 

    My loop carries the current investment balance from one month to the next. Every month the balance changes based on the investments growth and the new monthly contribution. 

    I will calculate the final investment value a second way by using the total amount I contributed plus the investment growth and check that it agrees with the final portfiolio value that was produced by my loop. 
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    initial_investment = 20000
    monthly_contribution = 500
    months = 60 
    investment_returns = {"Investment A": 0.08, "Investment B": 0.06, "Investment C": 0.10}
    return initial_investment, investment_returns, monthly_contribution, months


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(investment_returns):
    annual_return = investment_returns["Investment A"]
    print(annual_return)
    return (annual_return,)


@app.cell
def _(annual_return):
    monthly_return = annual_return / 12
    print(monthly_return)
    return (monthly_return,)


@app.cell
def _(initial_investment, monthly_contribution, monthly_return):
    one_month_balance = initial_investment
    one_month_balance = one_month_balance * (1 + monthly_return)
    one_month_balance = one_month_balance + monthly_contribution
    print(one_month_balance)
    return


@app.cell
def _(initial_investment, monthly_contribution, monthly_return, months):
    balance = initial_investment
    for month in range(1, months + 1):
        balance = balance * (1 + monthly_return)
        balance = balance + monthly_contribution
    print(f"Investment A final balance: ${balance:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
