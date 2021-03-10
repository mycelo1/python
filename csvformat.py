#!/usr/bin/python3

import argparse
import csv
import sys

def f_arg_normalize(arg):
    if len(arg) > 1:
        return arg[1:2]
    else:
        return arg

csv_lines = []
column_width = {}

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', type = ascii, default = ',', dest = 'delimiter', help = 'delimiter char')
arg_parser.add_argument('-q', type = ascii, default = '"', dest = 'quotechar', help = 'quotation char')
arg_parser.add_argument('-s', type = ascii, default = ' ', dest = 'separator', help = 'separator char')
arguments = arg_parser.parse_args()

delimiter = f_arg_normalize(arguments.delimiter)
quotechar = f_arg_normalize(arguments.quotechar)
separator = f_arg_normalize(arguments.separator)

csv_reader = csv.reader(
    sys.stdin,
    delimiter = delimiter,
    quotechar = quotechar)

for csv_row in csv_reader:
    csv_lines.append(csv_row)
    for csv_column in range(0, len(csv_row)):
        if csv_column in column_width:
            if column_width[csv_column] < len(csv_row[csv_column]):
                column_width[csv_column] = len(csv_row[csv_column])
        else:
            column_width[csv_column] = len(csv_row[csv_column])

for csv_row in csv_lines:
    output_line = ''
    for csv_column in range(0, len(csv_row)):
        output_line = output_line + csv_row[csv_column].ljust(column_width[csv_column]) + separator
    print(output_line)
