# -*- coding: utf-8 -*-

# Rounding Numbers. It rounds to nearest even digit
# rounding is not same as formatting

round(1.2313213, 2)
'{:0.3f}'.format(1.2313213)


# Working with Infinity and NaNs
a = float('inf')
b = float('-inf')
c = float('nan')

import math
math.isinf(b)

a,b,c # test for these values using math.isinf, math.isnan


# Picking Things at Random
import random # pick a random item out of a sequence: random.choice()
values = [1, 2, 3, 4, 5, 6]

random.choice(values)
random.choice(values)
random.choice(values)

# For a sampling of N items where selected items are removed from further consideration: random.sample()
random.sample(values, 2) 
random.sample(values, 2)
random.sample(values, 2)

# To shuffle items in a sequence in place, use random.shuffle()
random.shuffle(values)
values

# To produce random integers, use random.randint()
random.randint(0,10) # between 0 to 10

# To produce uniform floating-point values in the range 0 to 1, use random.random()
random.seed(0)
random.random()


# Converting Days to Seconds, and Other Basic Time Conversions
# For basic time arithmatic use datetime.timedelta
from datetime import timedelta
a = timedelta(days=2, hours=6)
b = timedelta(hours=4.5)

c = a + b
c.days
c.seconds
c.seconds / 3600
c.total_seconds() / 3600

# To represent specific dates and times, create datetime instances and use the
# standard mathematical operations to manipulate them
from datetime import datetime
a = datetime(2012,9,20)
print(a + timedelta(days=20))

b = datetime(2012, 12, 21) # Leap years are included already
d = b - a
d.days

# If you need to perform more complex date manipulations, such as dealing with time
# zones, fuzzy time ranges, calculating the dates of holidays etc use dateutil module
from dateutil.relativedelta import relativedelta
a = datetime(2012,9,20)
a + relativedelta(months=1)

b = datetime(2012, 12, 21)
d = b - a
d

d = relativedelta(b,a)
d


# Finding a date for the last occurrence of a day of the week
from datetime import datetime, timedelta
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
'Friday', 'Saturday', 'Sunday']
def get_previous_byday(dayname, start_date=None):
    if start_date is None:
        start_date = datetime.today()
    day_num = start_date.weekday()
    day_num_target = weekdays.index(dayname)
    days_ago = (7 + day_num - day_num_target) % 7
    if days_ago == 0:
        days_ago = 7
    target_date = start_date - timedelta(days=days_ago)
    return target_date

datetime.today()
get_previous_byday('Friday')
get_previous_byday('Sunday', datetime(2012, 12, 21))


# Same thing can be done easily using datetimeutil
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.rrule import *
d = datetime.now()
print(d + relativedelta(weekday=FR)) # Next friday
print(d + relativedelta(weekday=FR(-1))) # last friday



# Converting Strings into Datetimes
from datetime import datetime
text = '2018-09-20'
y = datetime.strptime(text, '%Y-%m-%d') # Usually not that efficient
z = datetime.now()
z - y

# If we know the string format beforehand we can do something like this
from datetime import datetime
def parse_ymd(s):
    year_s, mon_s, day_s = s.split('-')
    return datetime(int(year_s), int(mon_s), int(day_s))






