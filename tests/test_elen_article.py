#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `elen` package."""

from decimal import Decimal

import pytest

import elen


@pytest.mark.parametrize('number,representation', [
    (7, '+7'),
    (99, '++299'),
    (1234567890, '+++2101234567890'),
    (10 ** 999, '+++41000' + str(10 ** 999)),
])
def test_simple_elen_article(number, representation):
    """simple ELEN: examples included in the article"""
    assert elen.OriginalElen.simple(number) == representation, number


@pytest.mark.parametrize('number,representation', [
    (-1234567891, '---7898765432108'),
    (-1234567890, '---7898765432109'),
    (-1234567889, '---7898765432110'),
    (-11, '--788'),
    (-10, '--789'),
    (-9, '-0'),
    (-2, '-7'),
    (-1, '-8'),
    (0, '0'),
    (1, '+1'),
    (2, '+2'),
    (9, '+9'),
    (10, '++210'),
    (11, '++211'),
    (1234567889, '+++2101234567889'),
    (1234567890, '+++2101234567890'),
    (1234567891, '+++2101234567891'),
])
def test_int_elen_article(number, representation):
    """ELEN Integers: examples included in the article"""
    assert elen.OriginalElen.integer(number) == representation, number


@pytest.mark.parametrize('number,representation', [
    (Decimal('-0.9995'), '-0004+'),
    (Decimal('-0.999'), '-000+'),
    (Decimal('-0.0123'), '-9876+'),
    (Decimal('-0.00123'), '-99876+'),
    (Decimal('-0.0001233'), '-9998766+'),
    (Decimal('-0.000123'), '-999876+'),
    (Decimal('0'), '0'),
    (Decimal('0.000123'), '+000123-'),
    (Decimal('0.0001233'), '+0001233-'),
    (Decimal('0.00123'), '+00123-'),
    (Decimal('0.0123'), '+0123-'),
    (Decimal('0.999'), '+999-'),
    (Decimal('0.9995'), '+9995-'),
])
def test_small_decimals_article(number, representation):
    """ELEN Small Decimals: examples included in the article"""
    d_elen = elen.OriginalElen.decimal(number)
    small_d_elen = d_elen[0] + d_elen[2:]
    assert small_d_elen == representation, number


# original values from the article seem to be have multiple typos in them,
# because they would produce wrong lexicograpic ordering
@pytest.mark.parametrize('number,representation', [
    (Decimal('-100.5'), '--68994+'),
    (Decimal('-10.5'), '--7894+'),
    (Decimal('-3.145'), '-6854+'),  # original: '-3854+'
    (Decimal('-3.14'), '-685+'),  # original: '-385+'
    (Decimal('-1.01'), '-898+'),  # original: '-198+'
    (Decimal('-1'), '-8+'),  # original: '-1+'
    (Decimal('-0.0001233'), '-99998766+'),  # original: '-09998766+'
    (Decimal('-0.000123'), '-9999876+'),  # original: '-0999876+'
    (Decimal('0'), '0'),
    (Decimal('0.000123'), '+0000123-'),
    (Decimal('0.0001233'), '+00001233-'),
    (Decimal('1'), '+1-'),
    (Decimal('1.01'), '+101-'),
    (Decimal('3.14'), '+314-'),
    (Decimal('3.145'), '+3145-'),
    (Decimal('10.5'), '++2105-'),
    (Decimal('100.5'), '++31005-'),
])
def test_large_decimals_article(number, representation):
    """ELEN Large Decimals: examples included in the article"""
    assert elen.OriginalElen.decimal(number) == representation, number
