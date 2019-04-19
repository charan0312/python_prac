# Unpacking N element iterable into N elements

p = ['foo', 'bar', ('hello', 'world'), 5]

a, b, c, d = p

print(a, c)

# if there is a mismatch in number of elements: ERROR

a, b = p

# Unpacking works with any Iterable
s = 'Hello'

# TO discard elements, use a throwaway variable
_, _, a, b, c = s

print(a, c)

# Extended Itearable Unpacking
# IF we have a large N for an iterable: use "star epressions" (any position)
# We get a list for the starred variable (even if the list is empty)

record = ('Dave', 'dave@example.com', '773-555-1212', '847-555-1212')
name, email, *mobile_nums = record

print(name, mobile_nums)

*trailing, current = [10, 8, 7, 1, 9, 5, 10, 3]
print(sum(trailing)/len(trailing), current)

# Used for iterating over a seq of tuples of varying length

records = [('foo', 1, 2), ('bar', 'hello'), ('foo', 3, 4),]

def do_foo(x, y):
    print('foo', x, y)
    
def do_bar(s):
    print('bar', s)
    
for tag, *args in records:
    if tag == 'foo':
        do_foo(*args)
        
    elif tag == 'bar':
        do_bar(*args)
        
        
# Unpacking for string processing like splitting
line = 'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false'

uname, *fields, homedir, sh = line.split(':')

print(fields, homedir, sh,)


# To keep a limited history of the last few items 
# seen during iteration or during some other kind of processing
from collections import deque
q = deque(maxlen = 3) #maxlen = 3
q.append(1)
q.append(2)
q.append(3)
q
q.append(4)
q

# if no maxlen is given we get an unbounded list and we can
# append or pop on both sides

q = deque() 
q.append(1)
q.append(2)
q.append(3)
q.appendleft(4)
q
q.popleft() #gives first element of the list O(1)

# To get N largest or smallest items in a collection (N << size of collection)
import heapq
portfolio = [
{'name': 'IBM', 'shares': 100, 'price': 91.1},
{'name': 'AAPL', 'shares': 50, 'price': 543.22},
{'name': 'FB', 'shares': 200, 'price': 21.09},
{'name': 'HPQ', 'shares': 35, 'price': 31.75},
{'name': 'YHOO', 'shares': 45, 'price': 16.35},
{'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key=lambda s: s['price'])
expensive = heapq.nlargest(3, portfolio, key=lambda s: s['price'])

print(cheap, expensive)


# heap[0] is always the smallest element of the collection
# and subsequent heappops give the smallest of the collection

nums = [1, 8, 2, 23, 7, -4, 18, 23, 42, 37, 2]
heap = list(nums)
heapq.heapify(heap)
heap
heapq.heappop(heap)
heapq.heappop(heap)
heapq.heappop(heap)


# if N is comparable to size of collection, we can sort it and take the N
sorted(list(nums))[:6]
sorted(list(nums))[-6:]

# Implementing Priority queues (sort by priority and pop by highest priority)
# -priority is used as heappop always pops smallest item
#index is used to sort items with same priority
import heapq
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self.index = 0
    
    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self.index, item))
        self.index += 1
        
    def pop(self):
        return heapq.heappop(self._queue)[-1]
        

class Item:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return 'Item({!r})'.format(self.name)
    
    
q = PriorityQueue()   
q.push(Item('foo'), 1)
q.push(Item('bar'), 5)
q.push(Item('spam'), 4)
q.push(Item('grok'), 4)
q.pop()
q.pop()


# OrderedDict - to preserve the insertion order in a dictionary
# It is implemented by using double linked list (uses twice the memory)
from collections import OrderedDict

d = OrderedDict()
d['foo'] = 1
d['bar'] = 3
d['spam'] = 6
d['grok'] = 4

for k in d:
    print(k, d[k])
    
# OrderedDict is useful in json encoding to control the oder of fields
import json
json.dumps(d)


# for Dictionaries we can do reductions (max, min etc) only on keys
# we use zip to invert the keys and values (can be consumed only once)
prices = {
'ACME': 45.23,
'AAPL': 612.78,
'IBM': 205.55,
'HPQ': 37.20,
'FB': 10.75
}

min_price = min(zip(prices.values(), prices.keys()))
min_price

prices_sorted = sorted(zip(prices.values(), prices.keys()))
prices_sorted

#To find out what the two dictionaries have in common, simply perform common set
#operations using the keys() or items() methods like '&', '-' etc

a = {
'x' : 1,
'y' : 2,
'z' : 3
}


b = {
'w' : 10,
'x' : 11,
'y' : 2
}


a.items() & b.items()

a.keys() - b.keys() # keys in a and NOT in b [values don't have this capability as they are not a set]

c = {key:a[key] for key in a.keys() - {'z', 'w'}}
c

# Removing Duplicates from a seq while preserving order of remaining items
# if seq is hashable
def dedupe(items):
    seen = set()
    for item in items:
        if item not in seen:
            yield item
            seen.add(item)
    
a = [1, 5, 2, 1, 9, 1, 5, 10]

list(dedupe(a))


# if the seq is not hashable (dicts etc)
def dedupe(items, key=None):
    seen = set()
    for item in items:
        val = item if item is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)

a = [ {'x':1, 'y':2}, {'x':1, 'y':3}, {'x':1, 'y':2}, {'x':2, 'y':4}]
list(dedupe(a, key=lambda d: (d['x'],d['y'])))
list(dedupe(a, key=lambda d: (d['y'])))

# To read a file after eleminating duplicates
with open('somefile.txt', 'r') as f:
    for line in dedupe(f):
        print(line)


# Use slice objects insted of hardcoding
items = [0, 1, 2, 3, 4, 5, 6]
a = slice(2,6)

items[a]

items[a] = [10,11]
del items[a]
items

# Use slice.indices(len(str)) to avoid IndexError exceptions when indexing
s = 'HelloWorld'
a = slice(10, 50, 2)
a.indices(len(s))

for i in range(*a.indices(len(s))) :
    print(s[i])


# To get most frequent items in a seq
words = [
'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
'my', 'eyes', "you're", 'under'
]

# use collections.Counter (It is a dictionary with words as key) class' most_common method
from collections import Counter
word_counts = Counter(words)
word_counts.most_common(3)

word_counts['look']

morewords = ['why','are','you','not','looking','in','my','eyes']

# You can update the word count
word_counts.update(morewords)
word_counts

# Counter instances can be combined using mathematical operations
a = Counter(words)
b = Counter(morewords)

a, b
# combine counts
a + b


# Sorting a list of dictionaries by a key using itemgetter
rows = [
{'fname': 'Brian', 'lname': 'Jones', 'uid': 1003},
{'fname': 'David', 'lname': 'Beazley', 'uid': 1002},
{'fname': 'John', 'lname': 'Cleese', 'uid': 1001},
{'fname': 'Big', 'lname': 'Jones', 'uid': 1004}
]

from operator import itemgetter

rows_by_fname = sorted(rows, key=itemgetter('fname', 'lname'))
#Using Lambdas is slower than itemgetter
rows_by_lname = sorted(rows, key= lambda r: r['fname'])

rows_by_fname
rows_by_lname

# Sorting objects of the same class that don’t natively support comparison
class User:
    def __init__(self, user_id):
        self.user_id = user_id
    def __repr__(self):
        return 'User({!r})'.format(self.user_id)

users = [User(1), User(30), User(50)]
sorted(users, key = lambda u: u.user_id)

from operator import attrgetter
sorted(users, key = attrgetter('user_id'))


# Grouping Records Together Based on a Field

rows = [
{'address': '5412 N CLARK', 'date': '07/01/2012'},
{'address': '5148 N CLARK', 'date': '07/04/2012'},
{'address': '5800 E 58TH', 'date': '07/02/2012'},
{'address': '2122 N CLARK', 'date': '07/03/2012'},
{'address': '5645 N RAVENSWOOD', 'date': '07/02/2012'},
{'address': '1060 W ADDISON', 'date': '07/02/2012'},
{'address': '4801 N BROADWAY', 'date': '07/01/2012'},
{'address': '1039 W GRANVILLE', 'date': '07/04/2012'},
]

# Use itertools.groupby()
from operator import itemgetter
from itertools import groupby

rows.sort(key=itemgetter('date'))
for date,items in groupby(rows, key=itemgetter('date')):
    print(date)
    for i in items:
        print('    ', i)


#Filtering Sequence Elements
mylist = [1, 4, -5, 10, -7, 2, 3, -1]

# Using generators is more effective when N is large
pos = (n for n in mylist if n > 0)

for i in pos:
    print(i)


# OR filter method can be used and use list to get the list of results
list(filter(lambda n : n > 0, mylist))

# itertools.compress() can also be used to filter
addresses = [
'5412 N CLARK',
'5148 N CLARK',
'5800 E 58TH',
'2122 N CLARK'
'5645 N RAVENSWOOD',
'1060 W ADDISON',
'4801 N BROADWAY',
'1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]

from itertools import compress

more5 = [i>5 for i in counts]
list(compress(addresses, more5))


# Use generators when executing a reduction function (e.g., sum(), min(), max()) after
# transforming or filtering the data.

nums = [1, 3, 5, 6, 7]
s = sum(i*i for i in nums) # more efficient than list comprehension
s
# Determine if any .py files exist in a directory
import os
files = os.listdir('./')
if any(name.endswith('.py') for name in files):
    print('There be python!')
else:
    print('Sorry, no python.')
    

# For multiple dictionaries or mappings, to logically combine into a
# single mapping to perform certain operations use ChainMap
from collections import ChainMap
a = {'x': 1, 'z': 3 }
b = {'y': 2, 'z': 4 }

c = ChainMap(a,b)
print(c['x'])
print(c['y'])
print(c['z']) # If there are duplicates, always from a




















































 








