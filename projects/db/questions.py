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
    """)
    return


app._unparsable_cell(
    r"""
    Question: What is the total value of assets purchased by each member across all of their portfolios?
    """,
    name="_"
)


app._unparsable_cell(
    r"""
    Prediction: I predict that the join between members, portfolios, and trades to produce about 350 rows before grouping plus any rows representing members without portfolios or portfolios without trades. Each trade should appear once because it will belong to one portfolio and each portfolio belongs to one member. I will compare this prediction with the actual row count after running the query. 
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
