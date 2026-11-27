from decimal import Decimal, localcontext
from fractions import Fraction


def muller_term(n, x0, x1):
    """Вычислить член x_n по двум начальным значениям."""
    if n < 0:
        raise ValueError("Номер члена должен быть неотрицательным")
    if n == 0:
        return x0
    for _ in range(2, n + 1):
        x2 = 108 - (815 - 1500 / x0) / x1
        x0, x1 = x1, x2
    return x1


def main():
    exact = muller_term(30, Fraction(4), Fraction(17, 4))
    print("Приближённое значение с использованием Fraction:", float(exact))

    with localcontext() as ctx:
        ctx.prec = 55
        approximate = muller_term(30, Decimal(4), Decimal("4.25"))
    print("Приближённое значение с использованием Decimal:", float(approximate))


if __name__ == "__main__":
    main()
