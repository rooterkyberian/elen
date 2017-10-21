from hypothesis import given
from hypothesis.strategies import lists

import elen

from .utils import decimal_input


@given(lists(decimal_input))
def test_elen_decimal_ordering(decimals):
    """ELEN notation should preserve ordering when sorted lexicographically"""
    decimals.sort()
    elen_list = list(sorted(elen.decimal(d) for d in decimals))

    elen_to_d = {elen.decimal(d): d for d in decimals}
    assert [elen_to_d[e] for e in elen_list] == decimals
