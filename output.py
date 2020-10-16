#!/usr/bin/python3

"""
This program takes in a file with columns; time, voltage, and current. It then
parses all of the columns into their own array and performs several calculations
before printing the results of those calculations to the terminal.
"""

__author__ = "Nick Stolarow"
__copyright__ = "Copyright 2020, Nick Stolarow"
__credits__ = "Dr. Nirmala Kandadai"
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = "Nick Stolarow"
__email__ = "nickstolarow@gmail.com"
__status__ = "Production"

################################################################################
# Imports
################################################################################
import argparse
import math
import sys


################################################################################
# Globals
################################################################################
NUM_OPERATIONS = 3
BAR_LENGTH = 100


################################################################################
# Functions
################################################################################
def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('Filepath', help='The files location on the machine')

    return parser.parse_args()


def parse_file(filepath: str) -> list:
    main_list = []
    first_loop = True

    with open(filepath, 'r') as f:
        line = f.readline()

        while line:
            line = f.readline()
            values = line.split()

            if first_loop is True:
                first_loop = False
                for i in range(0, len(values)):
                    main_list.append(list())

            for a in reversed(main_list):
                if len(values) != 0:
                    a.append(float(values.pop()))

    return main_list


def peak_to_peak(values: list) -> float:
    return max(values) - min(values)


def phase_difference(list_of_columns: list, cols_to_operate: list) -> float:
    positive_first = None
    avg_a = 0.0
    avg_b = 0.0
    sign_change_index = -1
    time = list_of_columns[0]
    col_a = list_of_columns[cols_to_operate[0]]
    col_b = list_of_columns[cols_to_operate[1]]

    if col_a[0] > 0:
        positive_first = True
    else:
        positive_first = False

    for a in col_a:
        if positive_first:
            if a < 0:
                sign_change_index = col_a.index(a)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg_a = (time[t1] + time[t2]) / 2
                break
        else:
            if a > 0:
                sign_change_index = col_a.index(a)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg_a = (time[t1] + time[t2]) / 2
                break

    positive_first = None
    start_index = sign_change_index

    if col_b[start_index] > 0:
        positive_first = True
    else:
        positive_first = False

    for b in col_b[start_index:]:
        if positive_first:
            if b < 0:
                sign_change_index = col_b.index(b)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg_b = (time[t1] + time[t2]) / 2
                break
        else:
            if b > 0:
                sign_change_index = col_b.index(b)
                t1 = sign_change_index - 1
                t2 = sign_change_index
                avg_b = (time[t1] + time[t2]) / 2
                break

    return math.fabs(avg_a - avg_b)


def rms(values: list) -> float:
    sum_squared_values = 0.0

    for v in values:
        sum_squared_values += math.pow(v, 2)

    mean = sum_squared_values / len(values)

    return math.sqrt(mean)


def menu(list_of_columns: list):
    print('Press q To Exit.')

    while True:
        cols = input(
            'Specify Columns To Operate On (Separate Column Numbers By Commas (0 Is Left Most Column))?: ').lower()

        if cols == 'q':
            print('Goodbye!')
            sys.exit(0)

        cols_to_operate = cols.split(',')
        clean_list(cols_to_operate)

        try:
            cols_to_operate = [int(i) for i in cols_to_operate]
        except ValueError:
            print('Error: Input May Only Be Integers Separated By Commas.')
            continue

        if max(cols_to_operate) > len(list_of_columns) - 1 or min(cols_to_operate) < 0:
            print('Error: Column Specified Is Out Of Range.')
            continue

        print('Available Operations To Perform:\n1. RMS\n2. Peak-to-Peak\n3. Phase Difference')
        operation = input('Specify Operations To Perform (Separate Operation Numbers By Commas)?: ').lower()

        if operation == 'q':
            print('Goodbye!')
            sys.exit(0)

        print_bar()
        operations_to_perform = operation.split(',')
        clean_list(operations_to_perform)

        try:
            operations_to_perform = [int(j) for j in operations_to_perform]
        except ValueError:
            print('Error: Input May Only Be Integers And Commas.')
            print_bar()
            continue

        to_remove = []
        for k in operations_to_perform:
            if k > NUM_OPERATIONS or k < 1:
                print(f'Error: {k} Is An Unknown Operation')
                to_remove.append(k)

        for l in to_remove:
            operations_to_perform.remove(l)

        for op in operations_to_perform:
            for col in cols_to_operate:
                if op == 1:
                    print(f'RMS Of Column {col}: {rms(list_of_columns[col])}')
                elif op == 2:
                    print(f'Peak-to-Peak Of Column {col}: {peak_to_peak(list_of_columns[col])}')

            if op == 3:
                if len(cols_to_operate) == 2:
                    print(f'Phase Difference Of Column {cols_to_operate[0]} And {cols_to_operate[1]}: '
                          f'{phase_difference(list_of_columns, cols_to_operate)}')
                else:
                    print('Error: Could Not Calculate Phase Difference As It Requires Exactly Two Columns Of Data.')

        print_bar()


def clean_list(values: list):
    if '' in values:
        values.remove('')

    if ' ' in values:
        values.remove(' ')


def print_bar():
    print('-' * BAR_LENGTH)


################################################################################
# Run
################################################################################
if __name__ == '__main__':
    args = argument_parser()
    filepath = args.Filepath
    list_of_columns = parse_file(filepath)
    menu(list_of_columns)
