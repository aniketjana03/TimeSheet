import sys
import os

def generate_weekID(weekDates):
    date, month, year = weekDates[0].split('/')
    date_end, month_end, year_end = weekDates[6].split('/')
    if int(date) < 10:
        date = str(0) + str(date)
    if int(month) < 10:
        month = str(0) + str(month)
    if int(date_end) < 10:
        date_end = str(0) + str(date_end)
    code = str(year)+str(month)+str(date)+str(date_end)
    #DEBUG
    print(date, month, year, file=sys.stderr)
    print(code, file=sys.stderr)
    # We will return unique weekID code
    return code

def parse_sql(filename):
    data = open(filename, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
    return stmts
