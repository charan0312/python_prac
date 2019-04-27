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
class A:
    def __init__(self):
        self.x = 0
class B(A):
    def __init__(self):
        super().__init__()  # super makes sure that parents are initialized properly
        self.y = 1
        
b = B()
b.x

# Multiple inheritance and super()
class Base:
    def __init__(self):
        print('Hello from Base')

class A(Base):
    def __init__(self):
        super().__init__()
        print('Hello from A')
        
class B(Base):
    def __init__(self):
        super().__init__()
        print('Hello from B')
        
class C(A,B):
    def __init__(self):
        super().__init__()    # only one cal from super 
        print('Hello from C')
    
c = C()
c

# method resolution order (MRO) is simply a linear ordering of all the base classes (C3 Linearization)
# To implement inheritance, Python starts with the leftmost class and works its way leftto-
# right through classes on the MRO list until it finds the first attribute match
C.__mro__

# C3 Linearization is a merge sort of MROs from parent classes with 3 constraints:
# Child classes are checked before parent classes
# Multiple parents are checked in the order listed
# If there are 2 valid choices for the next class, pick one from first parent
class A:
    def spam(self):
        print('Hello from A')
        super().spam()
                
class B:
    def spam(self):
        print('Hello from B')
        
class C(A,B):
    pass

C.__mro__
c = C()
c.spam()



# Extending a Property in a Subclass
class Person:
    def __init__(self, name):
        self.name = name
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if not isinstance(val, str):
            raise TypeError('Expected a string')
        self._name = val
    
    @name.deleter
    def name(self):
        raise AttributeError('Can\'t delete attribute')
        
class SubPerson(Person):
    
    @property
    def name(self):
        print('getting name')
        return super(SubPerson, SubPerson).name.__get__(self)
    
    @name.setter
    def name(self, value):
        print('setting name to', value)
        super(SubPerson, SubPerson).name.__set__(self,value)

    @name.deleter
    def name(self):
        print('Deleting name')
        super(SubPerson, SubPerson).name.__delete__(self)

s = SubPerson('abcd')
s.name

# To extend just one of the methods of a property use @ClassA.methodA.getter etc
class SubPerson(Person):
    @Person.name.getter # set the decorator like this
    def name(self):
        print('Getting name')
        return super().name
    
    
    
# Using Lazily Computed Properties
# To define a read-only attribute as a property that only gets computed on access.
# Once accessed, you’d like the value to be cached and not recomputed on each access.
class lazyproperty: # This is a descriptor class as in the form of __get__(), __set__(), and __delete__() special methods. 
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value            

# 
import math
class Circle:
    def __init__(self, radius):
        self.radius = radius
    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2
    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius    

c = Circle(5)
vars(c)
c.area
c.perimeter
vars(c)
c.area # Not computed 2nd time



# Simplifying the Initialization of Data Structures
# To avoid writing highly repetitive and boilerplate __init__() functions
# generalize the initialization of data structures into a single __init__()
# function defined in a common base class

class Structure:
    # Class variable that specifies expected fields
    _fields = []
    def __init__(self, *args):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
            
        
#  Example Class definitions
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']
        
    class Point(Structure):
        _fields = ['x', 'y']
        
    class Circle(Structure):
        _fields = ['radius']
        def area(self):
            return math.pi * self.radius ** 2

s = Stock('ACME', 50, 91.1)
p = Point(2, 3)
c = Circle(4.5)
s2 = Stock('ACME', 50)

# keyword arguments as a means for adding additional
# attributes to the structure not specified in _fields.
class Structure:
# Class variable that specifies expected fields
    _fields= []
    def __init__(self, *args, **kwargs):
        if len(args) != len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        # Set the arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)      # self.__dict__.update(zip(self._fields,args))
        # Set the additional arguments (if any)
        extra_args = kwargs.keys() - self._fields
        for name in extra_args:
            setattr(self, name, kwargs.pop(name))
        if kwargs:
            raise TypeError('Duplicate values for {}'.format(','.join(kwargs)))
# Example use
if __name__ == '__main__':
    class Stock(Structure):
        _fields = ['name', 'shares', 'price']

    s1 = Stock('ACME', 50, 91.1)
    s2 = Stock('ACME', 50, 91.1, date='8/2/2012')


# Implementing a Data Model or Type System
# placing checks or assertions on the setting of certain instance attributes
# Base class. Uses a descriptor to set a value
class Descriptor:
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
# Descriptor for enforcing types
class Typed(Descriptor):
    expected_type = type(None)
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected ' + str(self.expected_type))
        super().__set__(instance, value)
# Descriptor for enforcing values
class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)
class MaxSized(Descriptor):
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name, **opts)
    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super().__set__(instance, value)

# These classes should be viewed as basic building blocks from which you construct a data
# model or type system. Continuing, here is some code that implements some different kinds of data
class Integer(Typed):
    expected_type = int
class UnsignedInteger(Integer, Unsigned):
    pass
class Float(Typed):
    expected_type = float
class UnsignedFloat(Float, Unsigned):
    pass
class String(Typed):
    expected_type = str
class SizedString(String, MaxSized):
    pass

# Using these type objects, it is now possible to define a class such as this
class Stock:
    # Specify constraints
    name = SizedString('name',size=8)
    shares = UnsignedInteger('shares')
    price = UnsignedFloat('price')
    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price

s = Stock('ACME', 50, 91.1)
s.name
s.shares = -10
s.name = 'ABRACADABRA'





































































