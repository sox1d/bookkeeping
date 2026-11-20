from fractions import Fraction

x0 = Fraction(4)
x1 = Fraction(17, 4)

for i in range(2, 31):
    x2 = 108 - (815 - 1500 / x0) / x1
    x0, x1 = x1, x2

print("Приближённое значение:", float(x1))