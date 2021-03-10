#!/usr/bin/python3

import argparse
import re
import sys

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-t', type = ascii, required = 'true', dest = 'table_name', help = 'table name')
arg_parser.add_argument('-c', type = ascii, required = 'true', dest = 'column_range', nargs = '+', help = 'list of columns to output (p1-p2)')
arg_parser.add_argument('-v', type = ascii, dest = 'first_value', help = 'optional fixed value for first column')
arg_parser.add_argument('-m', type = ascii, dest = 'regexp', help = 'only lines matching this regular expression')
arguments = arg_parser.parse_args()

if arguments.regexp is None:
    is_regexp = False
else:
    is_regexp = True
    regexp = re.compile(arguments.regexp.strip('"\''))
    
for line in sys.stdin:
    if (not is_regexp) or (regexp.search(line)):
        if arguments.first_value is None:
            sql_line = ''
        else:
            sql_line = '"' + arguments.first_value.strip('"\'') + '"'
        for arg_column in arguments.column_range:
            arg_column_split = arg_column.strip('"\'').split('-')
            column_start = int(arg_column_split[0])
            column_end = int(arg_column_split[1])
            column_value = line[(column_start - 1):column_end].strip()
            if len(sql_line) > 0:
                sql_line = sql_line + ', '
            if len(column_value) > 0:
                sql_line = sql_line + '"' + column_value + '"'
            else:
                sql_line = sql_line + 'NULL'
        print('INSERT INTO {} VALUES ({});'.format(arguments.table_name.strip('"\''), sql_line))
