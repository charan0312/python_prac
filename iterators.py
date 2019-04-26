# -*- coding: utf-8 -*-

# Manually Consuming an Iterator
# To process an iterable without a for loop use next()

with open('somefile.txt') as f:
    try:
        while True:
            line = next(f)
            print(line, end='')
    except StopIteration:   # StopIteration is used to signal the end of iteration
        pass
    
# For precise control we use next() instead of for loop
items = [1, 2, 3]
it = iter(items) # Get the iterator. Invokes items.__iter__()

next(it)  # Invokes it.__next__()
next(it)
next(it)
next(it)

# Delegating Iteration
# For a custom container object that internally holds a list, tuple, or some other
# iterable. To make iteration work with your new container, define __iter__() method
# that delegates iteration to the internally held container.
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []
        
    def __repr__(self):
        return 'Node{!r}'.format(self._value)
    
    def add_child(self, node):
        self._children.append(node)
    
    def __iter__(self):
        return iter(self._children)
    
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root: # __iter__() method simply forwards the iteration request to the internally held _children attribute
        print(ch)

# To implement a custom iteration pattern that’s different than the usual builtin
# functions (e.g., range(), reversed(), etc.)
def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step
    print('Done')
    
for i in frange(0,4,0.5):
    print(i)
    
c = frange(0,10,1)
next(c)


# Implementing the Iterator Protocol
class Node:
    def __init__(self, value):
        self._value = value
        self._children = []
        
    def __repr__(self):
        return 'Node{!r}'.format(self._value)
    
    def add_child(self, node):
        self._children.append(node)
    
    def __iter__(self):
        return iter(self._children)
    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()
    
if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))
    for ch in root.depth_first(): 
        print(ch)


# Iterating in Reverse
# Using reversed(). Reversed iteration only works if the object in question has a size that can be determined
# or if the object implements a __reversed__() special method. If neither of these can
# be satisfied, you’ll have to convert the object into a list first.
a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)
    
# Implementing __reversed__() let's us customize reversed()
class Countdown:
    def __init__(self, start):
        self.start = start
    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1
    # Reverse iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1
a = Countdown(5)
for i in reversed(a):
    print(i)


# Slicing an iterator by using itertools.islice()
def count(n):
    while True:
        yield n
        n += 1
c = count(0)

# Normal slicing won't work. The result of islice() is an iterator
# that produces the desired slice items, but it does this by consuming and discarding all
# of the items up to the starting slice index. Further items are then produced by the islice
# object until the ending index has been reached.
import itertools
for i in itertools.islice(c, 10, 20):
    print(i)


# Skipping the First Part of an Iterable using itertools.dropwhile()
# supply a function and an
# iterable. The returned iterator discards the first items in the sequence as long as the
# supplied function returns True. Afterward, the entirety of the sequence is produced.
from itertools import dropwhile
with open('somefile.txt') as f:
    for line in dropwhile(lambda line: line.startswith('H'), f):
        print(line, end='')

# If we know the exact number to skip we can use islice()
from itertools import islice
items = ['a', 'b', 'c', 1, 4, 10, 15]
for x in islice(items, 3, None): # [3:]
    print(x)


# Iterating Over All Possible Combinations or Permutations
items = ['a', 'b', 'c']
from itertools import permutations
for p in permutations(items):
    print(p)

# For permutations of smaller length
for p in permutations(items,2):
    print(p)
    
# To produce a sequence of combinations of items taken from the input
from itertools import combinations
for c in combinations(items,2):
    print(c)

# When producing combinations, chosen items are removed from the collection of possible
# candidates (i.e., if 'a' has already been chosen, then it is removed from consideration).
# The itertools.combinations_with_replacement() function relaxes this, and
# allows the same item to be chosen more than once
from itertools import combinations_with_replacement
for c in combinations_with_replacement(items, 2):
    print(c)

# Iterating Over the Index-Value Pairs of a Sequence
my_list = ['a', 'b', 'c']
for idx, val in enumerate(my_list):
    print(idx, val)

# To start the counter at 1
for idx, val in enumerate(my_list, 1):
    print(idx, val)
    
    
# For Iterating Over Multiple Sequences Simultaneously use zip()
xpts = [1, 5, 4, 2, 10, 7]
ypts = [101, 78, 37, 15, 62, 99]
for x, y in zip(xpts, ypts):
    print(x,y)
    

# Iterating on Items in Separate Containers one after the other
from itertools import chain
a = [1, 2, 3, 4]
b = ['x', 'y', 'z']
for x in chain(a, b):
    print(x)


# Creating Data Processing Pipelines
# To process these files, you could define a collection of small generator functions that
# perform specific self-contained tasks.
import os
import fnmatch
import gzip
import bz2
import re
def gen_find(filepat, top):
    '''
    Find all filenames in a directory tree that match a shell wildcard pattern
    '''
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path,name)

def gen_opener(filenames):
    '''
    Open a sequence of filenames one at a time producing a file object.
    The file is closed immediately when proceeding to the next iteration.
    '''
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
            yield f
            f.close()

def gen_concatenate(iterators):
    '''
    Chain a sequence of iterators together into a single sequence.
    '''
    for it in iterators:
        yield from it

def gen_grep(pattern, lines):
    '''
    Look for a regex pattern in a sequence of lines
    '''
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line

lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
for line in pylines:
    print(line)

# To extend this pipeline: feed the data in generator expressions
lognames = gen_find('access-log*', 'www')
files = gen_opener(lognames)
lines = gen_concatenate(files)
pylines = gen_grep('(?i)python', lines)
bytecolumn = (line.rsplit(None,1)[1] for line in pylines)
bytes = (int(x) for x in bytecolumn if x != '-')
print('Total', sum(bytes))



# Flattening a Nested Sequence
# isinstance(x, Iterable) simply checks to see if an item is iterable
from collections import Iterable
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):    # yield from flatten(x) is more cleaner
                yield i
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
# Produces 1 2 3 4 5 6 7 8
for x in flatten(items):
    print(x)


# Replacing Infinite while Loops with an Iterator



