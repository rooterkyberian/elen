from hypothesis.strategies import decimals

decimal_input = decimals(
    allow_infinity=False,
    allow_nan=False,
)
