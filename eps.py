from decimal import Decimal, localcontext


def machine_epsilon(precision):
    """Расстояние от единицы до следующего Decimal при заданной точности."""
    with localcontext() as ctx:
        ctx.prec = precision
        one = Decimal(1)
        return one.next_plus() - one


def main():
    n = abs(int(input('Укажите точность:\n')))
    print(machine_epsilon(n))
    print(f'10^-{n - 1}')


if __name__ == "__main__":
    main()
