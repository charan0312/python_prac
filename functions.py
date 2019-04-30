# -*- coding: utf-8 -*-

# Writing Functions That Accept Any Number of positional Arguments using *argument
# rest is a tuple of all the extra positional arguments passed. The code
# treats it as a sequence in performing subsequent calculations
def avg(first, *rest):
    return (first + sum(rest))/(1 + len(rest))

avg(1,2,3,4,5,0)
avg(1,2,5,0)

# To accept any number of keyword arguments, use an argument that starts with **
# attrs is a dictionary that holds the passed keyword arguments (if any)
import html
def make_element(name, value, **attrs):
    keyvals = [' %s="%s"' % item for item in attrs.items()]
    attr_str = ''.join(keyvals)
    element = '<{name}{attrs}>{value}</{name}>'.format(name=name,attrs=attr_str,value=html.escape(value))
    return element

make_element('item', 'Albatross', size='large', quantity=6)
make_element('p', '<spam>')

# If you want a function that can accept both any number of positional and keyword-only arguments, use * and ** together
def anyargs(*args, **kwargs):
    print(args)
    print(kwargs)
    
# A * argument can only appear as the last positional argument in a function definition.
# A ** argument can only appear as the last argument. A subtle aspect of function definitions
# is that arguments can still appear after a * argument
def a(x, *args, y):
    pass

a(1,2,3, y=0) # after args only key word arguments can be present
def b(x, *args, y, **kwargs):
    pass



# Writing Functions That Only Accept Keyword Arguments
# place the keyword arguments after a * argument or a single unnamed *
def recv(maxsize, *, block):
    'Receives a message'
    pass

recv(1024, True) # TypeError
recv(1024, block=True) # Ok

def mininum(*values, clip=None):
    m = min(values)
    if clip is not None:
        m = clip if clip > m else m
    return m
minimum(1, 5, 2, -5, 10) # Returns -5
minimum(1, 5, 2, -5, 10, clip=0) # Returns 0


# Attaching Informational Metadata to Function Arguments
# The Python interpreter does not attach any semantic meaning to the attached annotations.
# They are not type checks, nor do they make Python behave any differently than it did before.
def add(x:int, y:int) -> int:
    return x + y

# Function annotations are merely stored in a function’s __annotations__ attribute
add.__annotations__



# Returning Multiple Values from a Function
# To return multiple values from a function, simply return a tuple
def myfun():
    return 1,2,3 # returns a tuple (it’s actually the comma that forms a tuple, not the parentheses)

a,b,c = myfun()
a


# Defining Functions with Default Arguments
# Simply assign values in the definition and make sure that default arguments appear last
# the values assigned as defaults should always be immutable objects, such as None, True, False, numbers, or strings
def spam(a, b=42):
    print(a, b)
    
# to write code that merely tests whether an optional argument was given an interesting value or not
_no_value = object()
def spam(a, b=_no_value):
    if b is _no_value:
        print('No b value supplied')

spam(1)
spam(1, None)  #None is not same as _no_value

# the values assigned as a default are bound only once at the time of function definition
x = 42
def spam(a, b=42):
    print(a, b)
    
spam(1)
x = 0
spam(1) # x is still 42



# Defining Anonymous or Inline Functions
# Simple functions that do nothing more than evaluate an expression can be replaced by a lambda expression
add = lambda x,y: x + y
add(2,5)
add('sda', 'dsadsa')


# Capturing Variables in Anonymous Functions
# lambda expression is a free variable that gets bound at runtime, not definition time. Thus, the value of x in the lambda
# expressions is whatever the value of the x variable happens to be at the time of execution
# If you want an anonymous function to capture a value at the point of definition and
# keep it, include the value as a default value
x = 10
a = lambda y, x=x: x + y
x = 20
b = lambda y, x=x: x + y
a(10)
b(10)



# Making an N-Argument Callable Work As a Callable with Fewer Arguments using partial()
# partial() fixes the values for certain arguments and returns a new callable
# as a result. This new callable accepts the still unassigned arguments, combines them
# with the arguments given to partial(), and passes everything to the original function
def spam(a, b, c, d):
    print(a, b, c, d)

from functools import partial
s1 = partial(spam, 1)
s1(2,3,4)

points = [ (1, 2), (3, 4), (5, 6), (7, 8) ]
import math
def distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

# Here sort accepts functions that accept only one argument but we have 2
pt = (4,3)
points.sort(key=partial(distance, pt))



















