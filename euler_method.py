import math
from numpy import linspace


class WrongData(Exception):
    pass


def solve(a, b, h, x0, y0, func):
    if not (a <= x0 <= b):
        raise WrongData('x0 not in interval.')

    from timeit import default_timer
    start_time = default_timer()

    right_length = int((b - x0) / h)
    left_length = int((x0 - a) / h)

    xarr = []
    yarr = []

    x = x0
    y = y0
    for i in range(right_length):
        y = y + h * func.subs({('x', x), ('y', y)})
        x += h
        xarr.append(x)
        yarr.append(y)

    x = x0
    y = y0
    for i in range(left_length):
        y = y - h * func.subs({('x', x), ('y', y)})
        x -= h
        xarr.append(x)
        yarr.append(y)

    xarr.append(x0)
    yarr.append(y0)

    zipped_list = zip(xarr, yarr)
    sorted_pairs = sorted(zipped_list)
    tuples = zip(*sorted_pairs)
    xarr, yarr = [list(value) for value in tuples]

    end_time = default_timer()
    result_time = end_time - start_time

    return {'xarr': xarr, 'yarr': yarr, 'accuracy': h, 'time': result_time}
