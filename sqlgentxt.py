#!/usr/bin/python3

import argparse
import re
import sys

def tryFloat(number_string):
    try:
        return float(number_string)
    except ValueError:
        pass

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', type = ascii, required = True, dest = 'table_name', help = 'table name')
arg_parser.add_argument('-c', type = ascii, required = True, dest = 'column_range', nargs = '+', help = 'list of columns to output (p1-p2)')
arg_parser.add_argument('-m', type = ascii, dest = 'regexp', help = 'only lines matching this regular expression')
arg_parser.add_argument('-l', action = 'store_true', dest = 'line_number', default = False, help = 'add line number as first column')
arg_parser.add_argument('-v', type = ascii, dest = 'fixed_value', help = 'add fixed value as last column')
arg_parser.add_argument('-n', action = 'store_true', dest = 'detect_number', default = False, help = 'supress quotes for values detected as numeric')
arguments = arg_parser.parse_args()

if arguments.regexp is None:
    is_regexp = False
else:
    is_regexp = True
    regexp = re.compile(arguments.regexp.strip('"\''))
    
line_number = 0

for line in sys.stdin:
    line_number += 1
    if (not is_regexp) or (regexp.search(line)):
        if arguments.line_number:
            sql_line = '{}'.format(line_number)
        else:
            sql_line = ''
        for arg_column in arguments.column_range:
            arg_column_split = arg_column.strip('"\'').split('-')
            column_start = int(arg_column_split[0])
            column_end = int(arg_column_split[1])
            column_value = line[(column_start - 1):column_end].strip()
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
        print('INSERT INTO {} VALUES ({});'.format(arguments.table_name.strip('"\''), sql_line))
