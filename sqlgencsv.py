#!/usr/bin/python3

import argparse
import csv
import sys

def tryFloat(number_string):
    try:
        return float(number_string)
    except ValueError:
        pass

def f_arg_normalize(arg):
    if len(arg) > 1:
        return arg[1:2]
    else:
        return arg

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', type = ascii, required = True, dest = 'table_name', help = 'table name')
arg_parser.add_argument('-c', type = int, dest = 'column_number', nargs = '*', help = 'list of columns to output')
arg_parser.add_argument('-d', type = ascii, default = ',', dest = 'delimiter', help = 'CSV delimiter char')
arg_parser.add_argument('-q', type = ascii, default = '"', dest = 'quotechar', help = 'CSV quote char')
arg_parser.add_argument('-l', action = 'store_true', dest = 'line_number', default = False, help = 'add line number as first column')
arg_parser.add_argument('-v', type = ascii, dest = 'fixed_value', help = 'add fixed value as last column')
arg_parser.add_argument('-n', action = 'store_true', dest = 'detect_number', default = False, help = 'supress quotes for values detected as numeric')
arguments = arg_parser.parse_args()

delimiter = f_arg_normalize(arguments.delimiter)
quotechar = f_arg_normalize(arguments.quotechar)

csv_reader = csv.reader(
    sys.stdin,
    delimiter = delimiter,
    quotechar = quotechar)

line_number = 0

for csv_row in csv_reader:
    line_number += 1
    if arguments.line_number:
        sql_line = '{}'.format(line_number)
    else:
        sql_line = ''
    for csv_column in range(0, len(csv_row)):
        if (arguments.column_number is None) or ((csv_column + 1) in arguments.column_number):
            column_value = csv_row[csv_column].strip().replace('"', '\\"')
            if len(sql_line) > 0:
                sql_line = sql_line + ', '            
            if len(column_value) > 0:
                number_parse = tryFloat(column_value)
                if (arguments.detect_number) and (number_parse is not None):
                    sql_line = sql_line + column_value
                else:
                    sql_line = sql_line + '"' + column_value + '"'
            else:
                sql_line = sql_line + 'NULL'
    if arguments.fixed_value is not None:
        if len(sql_line) > 0:
            sql_line = sql_line + ', '
        sql_line = sql_line + '"' + arguments.fixed_value.strip('"\'') + '"'
    print('INSERT INTO {} VALUES ({});'.format(arguments.table_name.strip('\'"'), sql_line))
