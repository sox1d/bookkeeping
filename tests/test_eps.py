import unittest
from contextlib import redirect_stdout
from decimal import Decimal, localcontext
from io import StringIO
from unittest.mock import patch

from eps import machine_epsilon, main


class EpsilonTests(unittest.TestCase):
    def test_precision_28(self):
        """При 28 значащих цифрах шаг от единицы равен 10^(-27)."""
        with localcontext() as caller:
            caller.prec = 6
            self.assertEqual(machine_epsilon(28), Decimal("1e-27"))
            self.assertEqual(caller.prec, 6)

    def test_smallest_valid_precision(self):
        """При одной значащей цифре следующий сосед единицы — двойка."""
        self.assertEqual(machine_epsilon(1), Decimal(1))

    def test_negative_input_prints_corresponding_power(self):
        """Для ввода -4 обе строки ответа соответствуют точности 4."""
        output = StringIO()
        with patch("builtins.input", return_value="-4"), redirect_stdout(output):
            main()
        self.assertEqual(output.getvalue().splitlines(), ["0.001", "10^-3"])
