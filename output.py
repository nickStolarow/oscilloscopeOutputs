#!/usr/bin/python3

"""
This program takes in a file with columns; time, voltage, and current. It then
parses all of the columns into their own array and performs several calculations
before printing the results of those calculations to the terminal.
"""

# TODO: Allow user to specify what columns they want to operate on.
# TODO: Allow user to select what operations to perform on the specified columns.
# TODO: Operations consist of Peak-to-Peak, RMS, and Phase Difference.
# TODO: Phase difference is always between 2 columns
# TODO: (Time is always left most column)

__author__ = "Nick Stolarow"
__copyright__ = "Copyright 2020, Nick Stolarow"
__credits__ = "Dr. Nirmala Kandadai"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Nick Stolarow"
__email__ = "nickstolarow@gmail.com"
__status__ = "Production"

################################################################################
# Imports
################################################################################
import argparse
import math


################################################################################
# Functions
################################################################################
def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('Filepath', help='The files location on the machine')

    return parser.parse_args()


def parse_file(filepath: str) -> tuple:
    time = []
    voltage = []
    current = []

    with open(filepath, 'r') as f:
        line = f.readline()

        while line:
            line = f.readline()
            values = line.split()

            if len(values) != 0:
                current.append(float(values.pop()))
                voltage.append(float(values.pop()))
                time.append(float(values.pop()))

    return time, voltage, current


def peak_to_peak(values: list) -> float:
    return max(values) - min(values)


def voltage_zero_crossing(time: list, voltage: list) -> tuple:
    positive_first = None
    avg = 0.0
    sign_change_index = -1

    if voltage[0] > 0:
        positive_first = True
    else:
        positive_first = False

    for v in voltage:

        if positive_first:
            if v < 0:
                sign_change_index = voltage.index(v)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg = (time[t1] + time[t2]) / 2
                break
        else:
            if v > 0:
                sign_change_index = voltage.index(v)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg = (time[t1] + time[t2]) / 2
                break

    return avg, sign_change_index


def current_zero_crossing(time: list, current: list, start_index: int) -> float:
    positive_first = None
    avg = 0.0
    sign_change_index = -1

    if current[start_index] > 0:
        positive_first = True
    else:
        positive_first = False

    for c in current[start_index:]:

        if positive_first:
            if c < 0:
                sign_change_index = current.index(c)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg = (time[t1] + time[t2]) / 2
                break
        else:
            if c > 0:
                sign_change_index = current.index(c)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg = (time[t1] + time[t2]) / 2
                break

    return avg


def rms(values: list) -> float:
    sum_squared_values = 0.0

    for v in values:
        sum_squared_values += math.pow(v, 2)

    mean = sum_squared_values / len(values)

    return math.sqrt(mean)


################################################################################
# Run
################################################################################
if __name__ == '__main__':
    args = argument_parser()
    filepath = args.Filepath
    time, voltage, current = parse_file(filepath)
    print(f'Voltage Peak to Peak: {peak_to_peak(voltage)}V')
    print(f'Current Peak to Peak: {peak_to_peak(current)}I')
    v_zero_crossing, start_index = voltage_zero_crossing(time, voltage)
    c_zero_crossing = current_zero_crossing(time, current, start_index)
    print(f'When Voltage Crosses Zero: {v_zero_crossing}')
    print(f'When Current Crosses Zero: {c_zero_crossing}')

    if v_zero_crossing > c_zero_crossing:
        print(f'Phase Difference Between Voltage and Current: {v_zero_crossing - c_zero_crossing}')
    else:
        print(f'Phase Difference Between Current and Voltage: {c_zero_crossing - v_zero_crossing}')

    print(f'Voltage RMS: {rms(voltage)}')
    print(f'Current RMS: {rms(current)}')
