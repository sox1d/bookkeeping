import unittest
from decimal import Decimal, localcontext
from fractions import Fraction

from Muller import muller_term


# Для данных начальных условий x_n = (3^(n+1) + 5^(n+1)) / (3^n + 5^n).
EXACT_X30 = Fraction(3**31 + 5**31, 3**30 + 5**30)


class MullerTests(unittest.TestCase):
    def test_initial_terms(self):
        """При n = 0 и n = 1 возвращаются заданные начальные значения."""
        x0, x1 = Fraction(4), Fraction(17, 4)
        self.assertEqual(muller_term(0, x0, x1), x0)
        self.assertEqual(muller_term(1, x0, x1), x1)

    def test_fraction_x30_matches_closed_form(self):
        """Тридцатый член в Fraction в точности совпадает с явной формулой."""
        result = muller_term(30, Fraction(4), Fraction(17, 4))
        self.assertEqual(result, EXACT_X30)

    def test_decimal_x30_with_55_digits(self):
        """При точности 55 погрешность x_30 меньше 10^(-16)."""
        with localcontext() as ctx:
            ctx.prec = 55
            expected = Decimal(EXACT_X30.numerator) / EXACT_X30.denominator
            result = muller_term(30, Decimal(4), Decimal("4.25"))
            self.assertLess(abs(result - expected), Decimal("1e-16"))
