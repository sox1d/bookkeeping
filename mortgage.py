from decimal import Decimal, ROUND_HALF_UP, getcontext
import matplotlib.pyplot as plt
from datetime import *

getcontext().prec = 40


def money(x):
    return x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


s = Decimal(input('Размер кредита:'))
x = Decimal(input('Процентная ставка годовых:'))
y = Decimal(input('Количество лет:'))

while s <= 0 or x < 0 or y <= 0:
    print(f'\nВведите положительные значения')

    s = Decimal(input('Размер кредита:'))
    x = Decimal(input('Процентная ставка годовых:'))
    y = Decimal(input('Количество лет:'))

print(f'\nВаша запрос принят\n')

s = money(s)
r = x / Decimal(100) / Decimal(12)
m = y * 12

if r == 0:
    payment = money(s / m)
else:
    payment = money(s * (r / (1 - (1 + r) ** (-m))))

if r > 1:
    input('ВЫ ТОЧНО ХОТИТЕ ТАКОЙ КРЕДИТ?')
    print('Впрочем уже контракт подписан')

credit = s
total = Decimal(0)

months = [0]
history_credit = [credit]

percent_parts = []
base_parts = []

print()
print(
    f"{'Месяц':>6} "
    f"{'Платёж':>14} "
    f"{'Проценты':>14} "
    f"{'Основной долг':>16} "
    f"{'Остаток':>16}"
)

for n in range(1, int(m + 1)):
    percent = money(credit * r)
    if n == m:
        cur_pay = credit + percent
    else:
        cur_pay = min(payment, credit + percent)

    base = cur_pay - percent
    credit = credit - base
    total += cur_pay

    print(
        f"{n:>6} "
        f"{cur_pay:>14.2f} "
        f"{percent:>14.2f} "
        f"{base:>16.2f} "
        f"{credit:>16.2f}"
    )

    months.append(n)
    history_credit.append(credit)
    percent_parts.append(percent)
    base_parts.append(base)

    if credit == 0:
        break

print()
print(f"Ежемесячный платёж: {payment:.2f} руб.")
print(f"Всего выплачено: {total:.2f} руб.")
print(f"Переплата: {total - s:.2f} руб.")

plt.figure(figsize=(10, 5))
plt.plot(months, history_credit)
plt.title("Остаток по кредиту")
plt.xlabel("Месяц")
plt.ylabel("Остаток, руб.")
plt.grid()
plt.tight_layout()

plt.figure(figsize=(10, 5))
plt.plot(months[1:], percent_parts, label="Проценты")
plt.plot(months[1:], base_parts, label="Основной долг")
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
