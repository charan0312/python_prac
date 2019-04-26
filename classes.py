# -*- coding: utf-8 -*-

# Changing the String Representation of Instances
# __repr__() should produce text such that eval(repr(x)) == x
# If this is not possible or desired, then it is common to create a
# useful textual representation enclosed in < and > instead
# __str__() converts the instance to a string and output is same as str() and print()
# If no __str__() is defined, the output of __repr__() is used as a fallback.
class Pair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
# format code {0.x} specifies the x-attribute of argument 0. So, in the following function, the 0 is actually
# the instance self
        return 'Pair({0.x!r}, {0.y!r})'.format(self)
    def __str__(self):
        return '({0.x!s}, {0.y!s})'.format(self)
    
p = Pair(1,2)
print(p)



# Customizing String Formatting using __format__() and string method
_formats = {
'ymd' : '{d.year}-{d.month}-{d.day}',
'mdy' : '{d.month}/{d.day}/{d.year}',
'dmy' : '{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    def __format__(self, code):
        if code == '':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)
    
d = Date(2012, 12, 21)
format(d, 'mdy')



# Saving Memory When Creating a Large Number of Instances
# you are restricted to only those attribute names listed in the __slots__ specifier
class Date:
    __slots__ = ['year', 'month', 'day']
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

d = Date(2012,10,1)
d.abc = 'asas' # Throws an error


# Encapsulating Names in a Class
# any name that starts with a single leading underscore (_) should always be assumed to be internal implementation
# Python doesn’t actually prevent someone from accessing internal names. However, doing
# so is considered impolite, and may result in fragile code

class A:
    def __init__(self):
        self._internal = 0  # An internal attribute
        self.public = 1     # A public attribute
    
    def public_method(self):
        '''
        A public method
        '''
        return '{}'.format(self.public)
    def _internal_method(self):
        return '{}'.format(self._internal)

a = A()
a.public_method()
a._internal_method() # Should be used with caution

# The use of double leading underscores causes the name to be mangled to something else
# Here the name will be _B__private and _B__private_method()
# such attributes cannot be overridden via inheritance
# This can be used to hide the internal attributes from subclasses
class B:
    def __init__(self):
        self.__private = 0
    def __private_method(self):
        pass
    def public_method(self):
        self.__private_method()
    
b = B()
b.__private     # Throws an error
b._B__private   # Works fine

# To use a variable name that clashes with reserved keywords
lambda_ = 2.0 # Use a trailing underscore


# Creating Managed Attributes
# TO customize access to an attribute, define it as a “property.”

# Three related methods, all of which must have the same name.
# @first_name.setter and @first_name.deleter decorators won’t be defined unless first_name was already established
# as a property using @property
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    # Getter function and establishes first_name as a property
    @property
    def first_name(self):
        return self._first_name
    # Setter function
    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value
    # Deleter function (optional)
    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")
        
        
# A critical feature of a property is that it looks like a normal attribute, but access automatically
# triggers the getter, setter, and deleter methods.
a = Person('Guido')
a.first_name    # Calls getter
a.first_name = 10  # Calls setter
del a.first_name

# We can find the raw methods in the fget, fset, and fdel
# attributes of the property itself
Person.first_name.fget

# Properties can also be defined for existing get and set methods
class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)
    # Getter function
    def get_first_name(self):
        return self._first_name
    # Setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value
    # Deleter function (optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")
    # Make a property from existing get/set methods
    name = property(get_first_name, set_first_name, del_first_name)

b = Person('abcd')
b.set_first_name('sada')

# Properties can also be a way to define computed attributes. These are attributes that are
# not actually stored, but computed on demand
import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
        
    @property
    def area(self):
        return math.pi*self.radius**2
    @property
    def circumference(self):
        return 2*math.pi*self.radius
    
c = Circle(5)
c.area        
c.circumference


# Calling a Method on a Parent Class
# To call a method in a parent (or superclass), use the super() function














































