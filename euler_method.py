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


def accuracy_is_achieved_runge(yarr1, yarr2, accuracy):
    for i in range(len(yarr1)):
        if math.fabs(yarr1[i] - yarr2[i * 2]) > accuracy:
            return False
    return True


def solve_runge(a, b, h, x0, y0, accuracy, func):
    # print('Solving euler at h =', h)
    result1 = solve(a, b, h, x0, y0, func)
    result2 = solve(a, b, h / 2, x0, y0, func)

    if accuracy_is_achieved_runge(result1['yarr'], result2['yarr'], accuracy):
        result2['accuracy'] = accuracy
        print("Euler solved at h =", h / 2)
        return result2
    else:
        return solve_runge(a, b, h / 2, x0, y0, accuracy, func)
