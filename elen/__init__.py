# -*- coding: utf-8 -*-

__author__ = """Maciej Urbański"""
__email__ = 'rooter@kyberian.net'
__version__ = '0.1.0'

from decimal import Decimal
import io
import typing


def _to_int_and_fraction(d: Decimal) -> typing.Tuple[int, str]:
    """convert absolute decimal value into integer and decimal (<1)"""
    t = d.as_tuple()
    stringified = ''.join(map(str, t.digits))

    fraction = ''
    if t.exponent < 0:
        int_, fraction = stringified[:t.exponent], stringified[t.exponent:]
        fraction = fraction.rjust(-t.exponent, '0')
    else:
        int_ = stringified + t.exponent * '0'
    return int(int_ or 0), fraction


class OriginalElen:
    PLUS = '+'
    MINUS = '-'

    @classmethod
    def simple(cls, n: int) -> str:
        """
        The ELEN implementation as written in the pseudo code in original
        publication. Only natural numbers are supported.
        """
        buf = io.StringIO()
        if n > 0:
            buf.write(cls.PLUS)
        n_str = str(n)
        if len(n_str) > 1:
            buf.write(cls.simple(len(n_str)))
        buf.write(n_str)
        return buf.getvalue()

    @classmethod
    def flip(cls, n_str: str) -> str:
        n_str = ''.join(
            str(9 - int(char)) if char.isdigit() else char
            for char in n_str
        )
        return n_str.replace(cls.PLUS, cls.MINUS)

    @classmethod
    def integer(cls, n: int) -> str:
        """
        ELEN supporting negative as well as positive integers.
        """
        negative = n < 0
        if negative:
            n = -n

        n_str = cls.simple(n)
        if negative:
            n_str = cls.flip(n_str)
        return n_str

    @classmethod
    def decimal(cls, n: Decimal) -> str:
        """
        ELEN supporting large (and small) decimals.
        """
        int_, fraction = _to_int_and_fraction(n)
        if not fraction and int_ == 0:
            return '0'

        prefix = cls.simple(int_)
        if int_ == 0:
            prefix = cls.MINUS if n.is_signed() else cls.PLUS
            prefix += '0'

        representation = prefix + fraction
        if n.is_signed():
            representation = cls.flip(representation) + cls.PLUS
        else:
            representation += cls.MINUS

        return representation

    @classmethod
    def _decode_start(cls, d_int: str) -> typing.Tuple[int, str]:
        start = d_int.count(cls.PLUS)
        return cls._decode_pos(d_int, start, start + 1, start - 1)

    @classmethod
    def _decode_pos(cls, d_int, start, stop, left) -> typing.Tuple[int, str]:
        n = int(d_int[start:stop])
        if left == 0:
            return n, d_int[stop:]
        return cls._decode_pos(d_int, stop, stop + n, left-1)

    @classmethod
    def decode_integer(cls, representation: str) -> int:
        if representation == '0':
            return 0

        signed = representation[0] == cls.MINUS
        if signed:
            representation = cls.flip(representation).replace(
                cls.MINUS, cls.PLUS,
            )

        n, _ = cls._decode_start(representation)
        return -n if signed else n

    @classmethod
    def decode_decimal(cls, representation: str) -> Decimal:
        if representation == '0':
            return Decimal(0)

        representation = representation.rstrip(cls.PLUS + cls.MINUS)
        signed = representation[0] == cls.MINUS

        if signed:
            representation = cls.flip(representation).replace(
                cls.MINUS, cls.PLUS,
            )

        conv, fraction = cls._decode_start(representation)
        sign = '-' if signed else ''
        return Decimal('{}{}.{}'.format(sign, conv, fraction))


class Elen(OriginalElen):
    PLUS = '='


# shortcut for calling encoding methods:
decimal = Elen.decimal
decode_integer = Elen.decode_integer
decode_decimal = Elen.decode_decimal
integer = Elen.integer
simple = Elen.simple
