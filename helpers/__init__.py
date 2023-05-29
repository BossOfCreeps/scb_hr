from random import choices
from string import digits


def random_code(N: int = 6):
    return ''.join(choices(digits, k=N))
