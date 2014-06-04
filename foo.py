from random import randint
import sys
import matplotlib.pylab as plt

x = 7


def is_less_than_x(n):
    if n < x:
        return True
    else:
        return False

y = []


def find_x():
    #n = randint(0, 100)
    n = 2
    while n != x:
        if is_less_than_x(n):
            n = (n + 12) / 2
            y.append(n)
        else:
            n /= 2
            y.append(n)
    return n


print 'x =', find_x()
print y
i = range(1, len(y)+1)
print i
plt.plot(i, y)
plt.show()
