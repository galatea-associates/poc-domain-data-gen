import json
from datetime import timedelta, date


def daterange(start_date, day_count): 
    for n in range(day_count):
        print(start_date + timedelta(n))


start_date = date(2013,1,1)
day_count = 3650
daterange(start_date, day_count)