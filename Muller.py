from fractions import Fraction
from decimal import Decimal, getcontext

x0 = Fraction(4)
x1 = Fraction(17, 4)

for i in range(2, 31):
    x2 = 108 - (815 - 1500 / x0) / x1
    x0, x1 = x1, x2

print("Приближённое значение с использованием Fraction:", float(x1))

getcontext().prec = 55
# при изменение точности меняется итоговый результат

x0 = Decimal(4)
x1 = Decimal(4.25)

for i in range(2, 31):
    x2 = 108 - (815 - 1500 / x0) / x1
    x0, x1 = x1, x2

print("Приближённое значение с использованием Decimal:", float(x1))
