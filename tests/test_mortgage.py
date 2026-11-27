import unittest
from decimal import Decimal

from mortgage import repayment_schedule


class MortgageTests(unittest.TestCase):
    def test_annual_loan_at_twelve_percent(self):
        """Кредит 120 000 под 12% погашается за 12 месяцев с верной переплатой."""
        loan = Decimal("120000")
        payment, rows = repayment_schedule(loan, Decimal("12"), Decimal("1"))

        self.assertEqual(payment, Decimal("10661.85"))
        self.assertEqual([row.month for row in rows], list(range(1, 13)))
        self.assertEqual([row.amount for row in rows[:-1]], [payment] * 11)
        self.assertEqual(rows[0].interest, Decimal("1200.00"))
        self.assertEqual(rows[0].principal, Decimal("9461.85"))
        self.assertEqual(rows[-1].amount, Decimal("10661.91"))
        self.assertEqual(rows[-1].balance, 0)
        self.assertEqual(sum(row.amount for row in rows) - loan, Decimal("7942.26"))

    def test_zero_rate_closes_rounding_remainder(self):
        """Без процентов последняя выплата закрывает оставшуюся копейку."""
        payment, rows = repayment_schedule(Decimal("1000"), Decimal("0"), Decimal("0.25"))

        self.assertEqual(payment, Decimal("333.33"))
        self.assertEqual([row.amount for row in rows], [payment, payment, Decimal("333.34")])
        self.assertEqual([row.interest for row in rows], [0, 0, 0])
        self.assertEqual(rows[-1].balance, 0)

    def test_term_must_be_a_whole_number_of_months(self):
        """Для срока 1,1 года (13,2 месяца) программа сообщает об ошибке."""
        with self.assertRaisesRegex(ValueError, "месяцев"):
            repayment_schedule(Decimal("120000"), Decimal("12"), Decimal("1.1"))
