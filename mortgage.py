from decimal import Decimal, ROUND_HALF_UP, localcontext
from typing import NamedTuple


CALC_PRECISION = 40


class Payment(NamedTuple):
    month: int
    amount: Decimal
    interest: Decimal
    principal: Decimal
    balance: Decimal


def money(x):
    return x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def repayment_schedule(amount, annual_rate, years):
    """Вернуть обычный платёж и строки графика. Годовая ставка задана в процентах."""
    with localcontext() as ctx:
        ctx.prec = CALC_PRECISION
        credit = money(amount)
        months = years * 12
        if credit <= 0 or annual_rate < 0 or years <= 0:
            raise ValueError("Введите положительную сумму и срок, а ставку от 0%")
        if months != int(months):
            raise ValueError("Срок должен составлять целое число месяцев")
        months = int(months)
        r = annual_rate / Decimal(100) / Decimal(12)

        if r == 0:
            payment = money(credit / months)
        else:
            payment = money(credit * (r / (1 - (1 + r) ** (-months))))

        rows = []
        for month in range(1, months + 1):
            interest = money(credit * r)
            if month == months:
                current_payment = credit + interest
            else:
                current_payment = min(payment, credit + interest)
            principal = current_payment - interest
            credit -= principal
            rows.append(Payment(month, current_payment, interest, principal, credit))
            if credit == 0:
                break
        return payment, rows


def main():
    import matplotlib.pyplot as plt

    while True:
        s = Decimal(input('Размер кредита:'))
        x = Decimal(input('Процентная ставка годовых:'))
        y = Decimal(input('Количество лет:'))
        try:
            payment, rows = repayment_schedule(s, x, y)
        except ValueError as error:
            print(f'\n{error}')
        else:
            break

    print('\nВаша запрос принят\n')
    if x > 1200:
        input('ВЫ ТОЧНО ХОТИТЕ ТАКОЙ КРЕДИТ?')
        print('Впрочем уже контракт подписан')

    print()
    print(
        f"{'Месяц':>6} "
        f"{'Платёж':>14} "
        f"{'Проценты':>14} "
        f"{'Основной долг':>16} "
        f"{'Остаток':>16}"
    )
    for row in rows:
        print(
            f"{row.month:>6} "
            f"{row.amount:>14.2f} "
            f"{row.interest:>14.2f} "
            f"{row.principal:>16.2f} "
            f"{row.balance:>16.2f}"
        )

    with localcontext() as ctx:
        ctx.prec = CALC_PRECISION
        s = money(s)
        total = sum(row.amount for row in rows)
        overpayment = total - s

    print()
    print(f"Ежемесячный платёж: {payment:.2f} руб.")
    print(f"Всего выплачено: {total:.2f} руб.")
    print(f"Переплата: {overpayment:.2f} руб.")

    months = [row.month for row in rows]
    plt.figure(figsize=(10, 5))
    plt.plot([0] + months, [s] + [row.balance for row in rows])
    plt.title("Остаток по кредиту")
    plt.xlabel("Месяц")
    plt.ylabel("Остаток, руб.")
    plt.grid()
    plt.tight_layout()

    plt.figure(figsize=(10, 5))
    plt.plot(months, [row.interest for row in rows], label="Проценты")
    plt.plot(months, [row.principal for row in rows], label="Основной долг")
    plt.title("Состав ежемесячного платежа")
    plt.xlabel("Месяц")
    plt.ylabel("Сумма, руб.")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    img = plt.imread("em.jpg")
    plt.figure()
    plt.imshow(img)
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    main()
