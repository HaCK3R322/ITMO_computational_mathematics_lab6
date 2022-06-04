import math

import matplotlib.pyplot as plt
import sympy as sp

import adams_method
import euler_method


def lab6_interactive():
    function = input('Enter right part of function:\n>>> y\'(x) = ')
    function = sp.parse_expr(function,
                             transformations=sp.parsing.sympy_parser.standard_transformations)

    a = float(input('Enter a:\n>>> '))
    b = float(input('Enter b:\n>>> '))
    x0 = float(input('Enter x0:\n>>> y(x0) = y0, x0 = '))
    y0 = float(input('Enter y0:\n>>> y(x0) = y0, y0 = '))
    accuracy = float(input('Enter accuracy:\n>>> '))
    h = float(input('Enter start h:\n>>> '))

    from timeit import default_timer
    start_time = default_timer()

    euler_answer = euler_method.solve_runge(a, b, h, x0, y0, accuracy, function)
    # time
    end_time = default_timer()
    result_time = end_time - start_time
    euler_answer['time'] = result_time

    adams_answer = adams_method.solve_runge(a, b, h, x0, y0, accuracy, function)
    # time
    end_time = default_timer()
    result_time = end_time - start_time
    adams_answer['time'] = result_time

    need_yarr_true = input("Do you have true solved function to print? (y/anything else)\n>>> ")
    if need_yarr_true == 'y':
        true_func = input("Enter func here:\n>>> y(x) = ")
        true_func = sp.parse_expr(true_func,
                                  transformations=sp.parsing.sympy_parser.standard_transformations)
        true_yarr = []
        for x in euler_answer['xarr']:
            true_yarr.append(true_func.subs('x', x))
        plt.plot(euler_answer['xarr'], true_yarr, label='Correct function', color='g')

    plt.plot(euler_answer['xarr'], euler_answer['yarr'], label='euler method', color='r')
    plt.plot(adams_answer['xarr'], adams_answer['yarr'], label='adams method', color='b')

    plt.legend()
    plt.title("Results")
    plt.show()

    print('Took', euler_answer['time'], "seconds to achieve accuracy =", euler_answer['accuracy'], "for euler method")
    print('Took', adams_answer['time'], "seconds to achieve accuracy =", adams_answer['accuracy'], "for adams method")


def lab6_standard():
    function = '-2 * y'
    function = sp.parse_expr(function,
                             transformations=sp.parsing.sympy_parser.standard_transformations)

    # euler
    from timeit import default_timer
    start_time = default_timer()

    euler_answer = euler_method.solve_runge(-1, 1, 0.1, 0, 2, 0.01, function)

    end_time = default_timer()
    result_time = end_time - start_time
    euler_answer['time'] = result_time

    print("Euler method computation time:", euler_answer['time'], "Accuracy:", euler_answer['accuracy'])
    true_yarr = []
    for x in euler_answer['xarr']:
        true_yarr.append(2 * math.exp(-2 * x))

    plt.plot(euler_answer['xarr'], true_yarr, 'g')
    plt.plot(euler_answer['xarr'], euler_answer['yarr'], 'r')
    plt.title("Euler method (mode = standard)")
    plt.savefig('graphic.jpg', dpi=1200)
    plt.show()

    # adams
    start_time = default_timer()

    adams_answer = adams_method.solve_runge(-1, 1, 0.1, 0, 2, 0.01, function)

    end_time = default_timer()
    result_time = end_time - start_time
    adams_answer['time'] = result_time

    print("Adams method computation time:", adams_answer['time'], "Accuracy:", adams_answer['accuracy'])
    true_yarr.clear()
    for x in adams_answer['xarr']:
        true_yarr.append(2 * math.exp(-2 * x))

    plt.plot(adams_answer['xarr'], true_yarr, 'g')
    plt.plot(adams_answer['xarr'], adams_answer['yarr'], 'b')
    plt.title("Adams method (mode = standard, k = 4)")
    plt.savefig('graphic.jpg', dpi=1200)
    plt.show()

    print('\nAccuracy checking (for 10 element):')
    euler_x = euler_answer['xarr'][10]
    adams_x = adams_answer['xarr'][10]

    print('EULER:   x  =', str(euler_x))
    print('       y(x) =', euler_answer['yarr'][10])
    print('  true y(x) =', 2 * math.exp(-2 * euler_x))
    print(' difference =', euler_answer['yarr'][10] - 2 * math.exp(-2 * euler_x), '\n')

    print('ADAMS:   x  =', str(adams_x))
    print('       y(x) =', adams_answer['yarr'][10])
    print('  true y(x) =', 2 * math.exp(-2 * adams_x))
    print(' difference =', adams_answer['yarr'][10] - 2 * math.exp(-2 * adams_x), '\n')


if __name__ == '__main__':
    print("Modes:")
    print("1 - standard")
    print("2 - interactive\n")
    mode = input("Enter mode:\n>>> ")

    if mode == '1':
        lab6_standard()
    elif mode == '2':
        lab6_interactive()
    else:
        print("No such answer")
