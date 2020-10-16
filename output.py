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
import sys


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


def menu(list_of_columns: list):
    print('Press q To Exit.')

    while True:
        cols = input('Specify Columns To Operate On (Separate Column Numbers By Commas (0 Is Left Most Column))?: ').lower()

        if cols == 'q':
            print('Goodbye!')
            sys.exit(0)
        else:
            cols_to_operate = cols.split(',')

        if '' in cols_to_operate:
            cols_to_operate.remove('')

        if ' ' in cols_to_operate:
            cols_to_operate.remove(' ')

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
        else:
            print('-'*91)
            operations_to_perform = operation.split(',')

            if '' in operations_to_perform:
                operations_to_perform.remove('')

            if ' ' in operations_to_perform:
                operations_to_perform.remove(' ')

            try:
                operations_to_perform = [int(i) for i in operations_to_perform]
            except ValueError:
                print('Error: Input May Only Be Integers And Commas.')
                print('-'*91)
                continue

            for i in operations_to_perform:
                if i > 3 or i < 0:
                    print(f'Error: {i} Is An Unknown Operation')
                    break

            for op in operations_to_perform:
                for col in cols_to_operate:
                    if col == '':
                        continue

                    if op == 1:
                        print(f'RMS Of Column {col}: {rms(list_of_columns[col])}')
                    elif op == 2:
                        print(f'Peak-to-Peak Of Column {col}: {peak_to_peak(list_of_columns[col])}')
                    elif op == 3:
                        pass

                if op == 3:
                    if len(cols_to_operate) == 2:
                        col1, start_index = voltage_zero_crossing(list_of_columns[0], list_of_columns[1])
                        col2 = current_zero_crossing(list_of_columns[0], list_of_columns[2], start_index)

                        if col1 >= col2:
                            print(f'Phase Difference Of Column {cols_to_operate[0]} And {cols_to_operate[1]}: {col1 - col2}')
                        else:
                            print(f'Phase Difference Of Column {cols_to_operate[1]} And {cols_to_operate[0]}: {col2 - col1}')
                    else:
                        print('Error: Could Not Calculate Phase Difference As It Requires Exactly Two Columns Of Data.')

        print('-'*91)


################################################################################
# Run
################################################################################
if __name__ == '__main__':
    args = argument_parser()
    filepath = args.Filepath
    list_of_columns = parse_file(filepath)
    menu(list_of_columns)