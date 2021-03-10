#!/usr/bin/python3

import argparse
import csv
import sys

def f_arg_normalize(arg):
    if len(arg) > 1:
        return arg[1:2]
    else:
        return arg

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', type = ascii, required = 'true', dest = 'table_name', help = 'table name')
arg_parser.add_argument('-d', type = ascii, default = ',', dest = 'delimiter', help = 'delimiter char')
arg_parser.add_argument('-q', type = ascii, default = '"', dest = 'quotechar', help = 'quotation char')
arg_parser.add_argument('-c', type = int, dest = 'column_number', nargs = '*', help = 'list of columns to output')
arg_parser.add_argument('-v', type = ascii, dest = 'first_value', help = 'optional fixed value for first column')
arguments = arg_parser.parse_args()

delimiter = f_arg_normalize(arguments.delimiter)
quotechar = f_arg_normalize(arguments.quotechar)

csv_reader = csv.reader(
    sys.stdin,
    delimiter = delimiter,
    quotechar = quotechar)

for csv_row in csv_reader:
    if arguments.first_value is None:
        sql_line = ''
    else:
        sql_line = '"' + arguments.first_value.strip('"\'') + '"'
    for csv_column in range(0, len(csv_row)):
        if (arguments.column_number is None) or ((csv_column + 1) in arguments.column_number):
            column_value = csv_row[csv_column].strip().replace('"', '\\"')
            if len(sql_line) > 0:
                sql_line = sql_line + ', '            
            if len(column_value) > 0:
                sql_line = sql_line + '"' + column_value + '"'
            else:
                sql_line = sql_line + 'NULL'
    print('INSERT INTO {} VALUES ({});'.format(arguments.table_name.strip('\'"'), sql_line))
