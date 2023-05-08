import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QPushButton,
    QDoubleSpinBox,
    QLabel
)
from random import random
from objects import obj
from constants import (
    number_of_events,
    chi_square_005
)

spin_boxes: list[QDoubleSpinBox] = obj.objects.get('spinbox')
buttons: list[QPushButton] = obj.objects.get('button')
labels: list[QLabel] = obj.objects.get('label')


def start():
    trails = spin_boxes[-1].value()  # N
    expected_probabilities: list[float] = define_expected_probabilities()  # p
    intervals: list[float] = get_intervals(expected_probabilities)
    frequencies: list[int] = [0 for k in range(number_of_events)]  # n
    relative_frequencies: list[int] = []  # empirical probabilities: p^ = n/N

    for i in range(trails):
        frequencies[define_interval(intervals, random())] += 1

    for frequency in frequencies:
        relative_frequencies.append(frequency / trails)

    expected_characteristics: tuple = get_characteristics_of_discrete_rvs(expected_probabilities)
    relative_errors: tuple = get_relative_errors(expected_characteristics,
                                                 get_characteristics_of_discrete_rvs(relative_frequencies))

    average = 'Average: ' + str(round(expected_characteristics[0], 2)) + ' (error = ' + str(
        round(relative_errors[0], 2)) + ')'
    variance = 'Variance: ' + str(round(expected_characteristics[1], 2)) + ' (error = ' + str(
        round(relative_errors[1], 2)) + ')'
    labels[0].setText(average)
    labels[1].setText(variance)

    result: tuple = chi_squared_test(trails, frequencies, expected_probabilities)
    chi_squared = 'Chi-squared: ' + str(round(result[1], 2)) + ' > ' + str(round(result[2], 2)) + ' is ' + str(result[0])
    labels[2].setText(chi_squared)

    draw_bar(relative_frequencies)


def define_expected_probabilities() -> list[float]:
    expected_probabilities: list[float] = [0.0 for k in range(number_of_events)]
    count: float = 0
    for i in range(len(expected_probabilities)):
        count += spin_boxes[i].value()
        if count > 1:
            spin_boxes[i].setValue(0)
        else:
            expected_probabilities[i] = spin_boxes[i].value()

    if sum(expected_probabilities) < 1:
        expected_probabilities[-1] += 1 - sum(expected_probabilities)
        spin_boxes[number_of_events - 1].setValue(expected_probabilities[-1])
    return expected_probabilities


def get_intervals(expected_probabilities: list[float]) -> list[float]:
    intervals: list[float] = expected_probabilities[:]
    for i in range(1, len(intervals)):
        intervals[i] += intervals[i - 1]
    return intervals


def define_interval(intervals: list[float], alpha: float) -> int:
    if alpha <= intervals[0]:
        return 0
    for j in range(1, len(intervals)):
        if (alpha <= intervals[j]) and (alpha > intervals[j - 1]):
            return j
    return len(intervals) - 1


def get_characteristics_of_discrete_rvs(probabilities: list[float]) -> tuple:
    e: float = 0.0
    d: float = 0.0
    for i in range(1, len(probabilities) + 1):
        e += i * probabilities[i - 1]
        d += i ** 2 * probabilities[i - 1]
    d -= e ** 2
    return e, d


def get_relative_errors(expected_characteristics: tuple, empiric_characteristics: tuple) -> tuple:
    e_err = abs(empiric_characteristics[0] - expected_characteristics[0]) / abs(expected_characteristics[0])
    d_err = abs(empiric_characteristics[1] - expected_characteristics[1]) / abs(expected_characteristics[1])
    return e_err, d_err


def chi_squared_test(trails: int, frequencies: list[int], expected_probabilities: list[float]) -> tuple:
    x = 0
    for i in range(number_of_events):
        x += frequencies[i] ** 2 / (trails * expected_probabilities[i])
    x -= trails
    x_ = chi_square_005.get(number_of_events - 1)
    if x > x_:
        return True, x, x_
    return False, x, x_


def draw_bar(relative_frequencies: list[int]) -> None:
    courses = [f"{i}" for i in range(1, len(relative_frequencies) + 1)]
    values = relative_frequencies
    plt.bar(courses, values)
    plt.xlabel("Events")
    plt.ylabel("Frequencies")
    plt.show()


buttons[0].clicked.connect(start)
