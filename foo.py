# Kanjoya Binary Search Problem
"""
    Given x which is an unbounded integer > 0
    and a method isLessThanX(int y) which takes in an arg y
    find x
"""
from random import randint
import sys


x = randint(1, sys.maxint)
print x


def is_less_than_x(y):
    if y < x:
        return True
    else:
        return False


def find_x():
    global lower
    global upper
    lower = 1
    upper = sys.maxint
    y = randint(lower, upper)
    while y != x:
        if is_less_than_x(y):
            lower = y
            y = (lower + upper) / 2
            #print y
        else:
            upper = y
            y = (lower + upper) / 2
            #print y
    return y

print find_x()