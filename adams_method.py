import math

import sympy as sp
import euler_method


def get_delta(func_arr, power):
    if power == 0:
        return func_arr[-1]
    elif power == 1:
        return func_arr[-1] - func_arr[-2]
    elif power == 2:
        return func_arr[-1] - 2 * func_arr[-2] + func_arr[-3]
    elif power == 3:
        return func_arr[-1] - 3 * func_arr[-2] + 3 * func_arr[-3] - func_arr[-4]
    else:
        raise ValueError('Cannot calculate delta!')


def adams_formula(yi, h, func_arr):
    y = yi \
        + h * get_delta(func_arr, 0) \
        + (h ** 2 / 2) * get_delta(func_arr, 1) \
        + 5 * (h ** 3 / 12) * get_delta(func_arr, 2) \
        + 3 * (h ** 4 / 8) * get_delta(func_arr, 3)
    return y


def calculate_length(a, b, h):
    length = math.ceil(math.fabs((b - a) / h))
    # if length % 2 != 0:
    #     length -= 1
    return length


def get_first_4_values(x0, y0, h, accuracy, func):
    first_4_values_data = euler_method.solve_runge(x0, x0 + 3 * h, h, x0, y0, accuracy, func)
    step = len(first_4_values_data['xarr']) // 4

    xarr, yarr = [], []

    xarr.append(first_4_values_data['xarr'][0 * step])
    xarr.append(first_4_values_data['xarr'][1 * step])
    xarr.append(first_4_values_data['xarr'][2 * step])
    xarr.append(first_4_values_data['xarr'][3 * step])

    yarr.append(first_4_values_data['yarr'][0 * step])
    yarr.append(first_4_values_data['yarr'][1 * step])
    yarr.append(first_4_values_data['yarr'][2 * step])
    yarr.append(first_4_values_data['yarr'][3 * step])

    return {'xarr': xarr, 'yarr': yarr}


def solve(a, b, h, x0, y0, func):
    """
    Solves first-order homogeneous differential equation. (first 4 approximations based on euler method)

    :return: 'xarr' - x values on [a;b] with step h, 'yarr' - calculated y values, 'accuracy'
    :param a: left border of the interval
    :type a: float
    :param b: right border of the interval
    :type b: float
    :param h: step size
    :type h: float
    :param x0: x0 in y(x0) = y0
    :type x0: float
    :param y0: y0 in y(x0) = y0
    :type y0: float
    :param func: right part of y' = func(x, y)
    :type func: sp.Expr
    """

    from timeit import default_timer
    start_time = default_timer()

    xarr = []
    yarr = []
    func_arr = []

    # RIGHT DIRECTION
    # first_4_values_data = euler_method.solve(x0, x0 + 3 * h, h, x0, y0, func)
    # first_4_xarr = first_4_values_data['xarr']
    # first_4_yarr = first_4_values_data['yarr']
    # for i in range(4):
    #     xarr.append(first_4_xarr[i])
    #     yarr.append(first_4_yarr[i])
    #     func_arr.append(func.subs({('x', first_4_xarr[i]), ('y', first_4_yarr[i])}))

    first_4_values_data = get_first_4_values(x0, y0, h, h, func)
    first_4_xarr = first_4_values_data['xarr']
    first_4_yarr = first_4_values_data['yarr']
    for i in range(4):
        xarr.append(first_4_xarr[i])
        yarr.append(first_4_yarr[i])
        func_arr.append(func.subs({('x', first_4_xarr[i]), ('y', first_4_yarr[i])}))

    x = first_4_xarr[-1]  # setting x0 = last_x
    right_length = calculate_length(first_4_xarr[-1], b, h)
    for i in range(3, right_length):
        y = yarr[-1]
        yarr.append(adams_formula(y, h, func_arr))

        x += h
        xarr.append(x)
        func_arr.append(func.subs({('x', x), ('y', y)}))

    # LEFT DIRECTION
    first_4_values_data = get_first_4_values(x0, y0, -h, h, func)
    first_4_xarr = first_4_values_data['xarr']
    first_4_yarr = first_4_values_data['yarr']
    for i in range(4):
        xarr.append(first_4_xarr[i])
        yarr.append(first_4_yarr[i])
        func_arr.append(func.subs({('x', first_4_xarr[i]), ('y', first_4_yarr[i])}))

    x = first_4_xarr[-1]  # setting x0 = last_x
    left_length = calculate_length(a, first_4_xarr[-1], h)
    for i in range(3, left_length):
        y = yarr[-1]
        yarr.append(adams_formula(y, -h, func_arr))

        x -= h
        xarr.append(x)
        func_arr.append(func.subs({('x', x), ('y', y)}))

    zipped_list = zip(xarr, yarr)
    sorted_pairs = sorted(zipped_list)
    tuples = zip(*sorted_pairs)
    xarr, yarr = [list(value) for value in tuples]

    end_time = default_timer()
    result_time = end_time - start_time

    result = {'xarr': xarr, 'yarr': yarr, 'accuracy': h ** 4, 'time': result_time}
    return result


def accuracy_is_achieved_runge(yarr1, yarr2, accuracy):
    for i in range(len(yarr1) - 1):
        if math.fabs((yarr1[i] - yarr2[i * 2])) > accuracy:
            return False
    return True


def solve_runge_with_help(a, b, h, x0, y0, accuracy, func, last_res):
    result1 = last_res
    result2 = solve(a, b, h / 2, x0, y0, func)

    if accuracy_is_achieved_runge(result1['yarr'], result2['yarr'], accuracy):
        result2['accuracy'] = accuracy
        return result2
    else:
        return solve_runge_with_help(a, b, h / 2, x0, y0, accuracy, func, result2)


def solve_runge(a, b, h, x0, y0, accuracy, func):
    if h > accuracy:
        h = accuracy

    result1 = solve(a, b, h, x0, y0, func)
    result2 = solve(a, b, h / 2, x0, y0, func)

    if accuracy_is_achieved_runge(result1['yarr'], result2['yarr'], accuracy):
        result2['accuracy'] = accuracy
        # print("Adams solved at h =", h / 2)
        return result2
    else:
        return solve_runge_with_help(a, b, h / 2, x0, y0, accuracy, func, result2)
