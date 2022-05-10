import numpy as np


class a():
    x: int

    def __init__(self, x: int = 0) -> None:
        self.x = x

def func(a: a) -> None:
    a.x += 1

s= a(2)
print(s.x)
func(s)
print(s.x)
