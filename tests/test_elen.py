from decimal import Decimal

import pytest

import elen

integers_to_elen_test1 = [
    (Decimal('-1000'), '--58999='),
    (Decimal('-101'), '--6898='),
    (Decimal('-100'), '--6899='),
    (Decimal('-11'), '--788='),
    (Decimal('-10'), '--789='),
    (Decimal('-1'), '-8='),
    (Decimal('0'), '0'),
    (Decimal('0.1'), '=01-'),
    (Decimal('1'), '=1-'),
    (Decimal('5'), '=5-'),
    (Decimal('10'), '==210-'),
    (Decimal('15'), '==215-'),
    (Decimal('15.23'), '==21523-'),
    (Decimal('15.235'), '==215235-'),
]


@pytest.mark.parametrize('number,representation', integers_to_elen_test1)
def test_decimal(number, representation):
    """decimal to ELEN"""
    assert elen.decimal(number) == representation, number


@pytest.mark.parametrize('number,representation', integers_to_elen_test1)
def test_decode_decimal(number, representation):
    """ELEN to decimal"""
    d = elen.decode_decimal(representation)
    assert d == number
    assert isinstance(d, Decimal), number
