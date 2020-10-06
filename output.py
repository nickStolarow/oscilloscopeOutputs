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
def argument_parser() -> list:
    parser = argparse.ArgumentParser()
    parser.add_argument('Filepath', help='The files location on the machine')

    return parser.parse_args()


def parse_file(filepath:str) -> tuple:
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

    return (time, voltage, current)


def peak_to_peak(values:list) -> float:
    return max(values) - min(values)


def phase_difference(time:list, values:list) -> float:
    positive_first = None
    avg = 0.0

    if values[0] > 0:
        positive_first = True
    else:
        positive_first = False

    for v in values:

        if positive_first:
            if v < 0:
                t1 = values.index(v) - 1
                t2 = values.index(v)
                avg = (time[t1] + time[t2]) / 2
                break
        else:
            if v > 0:
                t1 = values.index(v) - 1
                t2 = values.index(v)
                avg = (time[t1] + time[t2]) / 2
                break

    return avg


def rms(values:list) -> float:
    sum_squared_values = 0.0
    
    for v in values:
        sum_squared_values += math.pow(v,2)
    
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
    voltage_avg_time = phase_difference(time, voltage)
    current_avg_time = phase_difference(time, current)
    print(f'When Voltage Crosses Zero: {voltage_avg_time}')
    print(f'When Current Crosses Zero: {current_avg_time}')

    if voltage_avg_time > current_avg_time:
        print(f'Phase Difference Between Voltage and Current: {voltage_avg_time - current_avg_time}')
    else:
        print(f'Phase Difference Between Current and Voltage: {current_avg_time - voltage_avg_time}')

    print(f'Voltage RMS: {rms(voltage)}')
    print(f'Current RMS: {rms(current)}')
