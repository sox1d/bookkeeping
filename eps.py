from decimal import Decimal, getcontext

n = int(input('Укажите точность:\n'))

getcontext().prec = abs(n)

print(Decimal(1).next_plus() - Decimal(1))
print(f'10^-{n - 1}')
