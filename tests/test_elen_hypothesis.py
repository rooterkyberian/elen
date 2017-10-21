from hypothesis import given
from hypothesis.strategies import integers

import elen

from .utils import decimal_input


@given(integers())
def test_elen_integer(n):
    n_elen = elen.integer(n)
    assert isinstance(n_elen, str)
    assert elen.decode_integer(n_elen) == n


@given(decimal_input)
def test_elen_decimal(d):
    d_elen = elen.decimal(d)
    assert isinstance(d_elen, str), d
    assert elen.decode_decimal(d_elen) == d
