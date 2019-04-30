# -*- coding: utf-8 -*-

# Reading and Writing CSV Data using csv module
import csv
from collections import namedtuple
with open('./stocks.csv') as f:
    f_csv = csv.reader(f)   # First create a csv reader object
    headers = next(f_csv)
    # this only works if the column headers are valid Python identifiers
    Row = namedtuple('Row', headers) # using named tuples is cleaner than tuples (row.Symbol, row.Price, etc)
    for r in f_csv:
        row = Row(*r)  #Row(Symbol='AXP', Price='62.58', Date='6/11/2007', Time='9:36am', Change='-0.46', Volume='935000')
        print(row.Symbol, row.Price)

# If headers are not in valid format, first change them
import re
with open('stock.csv') as f:
    f_csv = csv.reader(f)
    headers = [ re.sub('[^a-zA-Z_]', '_', h) for h in next(f_csv) ] 
    Row = namedtuple('Row', headers)
    for r in f_csv:
        row = Row(*r)  #Row(Symbol='AXP', Price='62.58', Date='6/11/2007', Time='9:36am', Change='-0.46', Volume='935000')
        print(row.Symbol, row.Price)


        
# Example of reading tab-separated values
with open('stock.tsv') as f:
    f_tsv = csv.reader(f, delimiter='\t')
    for row in f_tsv:
        # Process row
        pass

# We can use dictionary as well to read the data as a sequence
import csv
with open('./stocks.csv') as f:
    f_csv = csv.DictReader(f)
    for row in f_csv:
        print(row['Symbol'], row['Price'])  # We can read the fields like a dictionary values
        

# To write CSV data, use the csv module but create a writer object
headers = ['Symbol','Price','Date','Time','Change','Volume']
rows = [('AA', 39.48, '6/11/2007', '9:36am', -0.18, 181800),
('AIG', 71.38, '6/11/2007', '9:36am', -0.15, 195500),
('AXP', 62.58, '6/11/2007', '9:36am', -0.46, 935000),
]

with open('new_stocks.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)
               
# if rows are in a dictionary
headers = ['Symbol', 'Price', 'Date', 'Time', 'Change', 'Volume']
rows = [{'Symbol':'AA', 'Price':39.48, 'Date':'6/11/2007',
'Time':'9:36am', 'Change':-0.18, 'Volume':181800},
{'Symbol':'AIG', 'Price': 71.38, 'Date':'6/11/2007',
'Time':'9:36am', 'Change':-0.15, 'Volume': 195500},
{'Symbol':'AXP', 'Price': 62.58, 'Date':'6/11/2007',
'Time':'9:36am', 'Change':-0.46, 'Volume': 935000},
]
with open('stocks.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)     
        

# csv always treats the fields as a string, we'll have to change them manually
col_types = [str, float, str, str, float, int]
with open('stocks.csv') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)
    for row in f_csv:
    # Apply conversions to the row items
        row = tuple(convert(value) for convert, value in zip(col_types, row))
        
        pass
        
        
   
# Reading and Writing JSON Data
# The two main functions are json.dumps() and json.loads(), mirroring the interface used in
# other serialization libraries, such as pickle.
import json
data = {
'name' : 'ACME',
'shares' : 100,
'price' : 542.23
}
json_str = json.dumps(data) # Python data structure into JSON
data = json.loads(json_str)  #JSON-encoded string back into a Python data structure
   
# While working with files instead of strings, you can alternatively use json.dump()
# and json.load() to encode and decode JSON data        
# Writing JSON data
with open('data.json', 'w') as f:
    json.dump(data, f)
# Reading data back
with open('data.json', 'r') as f:
    data = json.load(f)
        
# JSON encoding supports the basic types of None, bool, int, float, and str, as well as
# lists, tuples, and dictionaries containing those types      
d = {'a': True,
'b': 'Hello',
'c': None}

json.dumps(d)     # True is mapped to true, False is mapped to false, and None is mapped to null 


# Use pprint for examining nested jsons
from urllib.request import urlopen
import json
u = urlopen('http://search.twitter.com/search.json?q=python&rpp=5')
resp = json.loads(u.read().decode('utf-8'))
from pprint import pprint
pprint(resp)
        
# JSON decoding will create dicts or lists from the supplied data. If you want
# to create different kinds of objects, supply the object_pairs_hook or object_hook to json.loads()      
# Decode by preserving the order using an OrderedDict
s = '{"name": "ACME", "shares": 50, "price": 490.1}'
from collections import OrderedDict
data = json.loads(s, object_pairs_hook=OrderedDict)
data
        
# JSON dictionary into a Python object
class JSONObject:
    def __init__(self, d):
        self.__dict__ = d
        
data = json.loads(s, object_hook=JSONObject)
data.name
data.shares
data.price

print(json.dumps(data))
print(json.dumps(data, indent=4)) # Using indent gives formatted output


# If you want to serialize instances, you can supply a function that takes an instance as input and returns a dictionary that can be serialized
def serialize_instance(obj):
    d = {'__classname__': type(obj).__name__ }
    d.update(vars(obj))
    return d

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3,7)
json.dumps(p) # Throws an error
json.dumps(serialize_instance(p))

# To get the instance back
# Dictionary mapping names to known classes
classes = {
'Point' : Point
}

def unserialize_object(d):
    clsname = d.pop('__classname__', None)
    if clsname:
        cls = classes[clsname]
        obj = cls.__new__(cls)   # Make instance without calling __init__
        for k,v in d.items():
            setattr(obj,k,v)
            return obj
    else:
        return d

p = Point(2,3)
s = json.dumps(p, default=serialize_instance)
s
a = json.loads(s, object_hook=unserialize_object)
a
a.x
a.y


























