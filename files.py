# -*- coding: utf-8 -*-

# Reading and Writing Text Data
# To append to the end of an existing file, use open() with mode at
# Read the entire file as a single string
with open('somefile.txt', 'rt') as f:
    data = f.read()
    
# Iterate over the lines of the file
with open('somefile.txt', 'rt') as f:
    for line in f:
        # process line

# Write chunks of text data
with open('somefile.txt', 'wt') as f:
    f.write(text1)        

# encoded files
with open('somefile.txt', 'rt', encoding='latin-1') as f:
    
# Replace bad chars with Unicode U+fffd replacement char
f = open('sample.txt', 'rt', encoding='ascii', errors='replace')

# Ignore bad chars entirely
g = open('sample.txt', 'rt', encoding='ascii', errors='ignore')



# Printing to a File
# Use the file keyword argument to print()
with open('somefile.txt', 'rt') as f:
    print('Hello World!', file=f)


# Printing with a Different Separator or Line Ending
print('ACME', 50, 91.5, sep=',', end='!!\n')



# Reading and Writing Binary Data
# Use the open() function with mode rb or wb to read or write binary data
# to read or write text from a binary-mode file, decode or encode it.
with open('somefile.bin', 'rb') as f:
    data = f.read(16)
    text = data.decode('utf-8')
    print(text)

with open('somefile.bin', 'wb') as f:
    text = 'Hello World'
    f.write(text.encode('utf-8'))
    
    

# You want to write data to a file, but only if it doesn’t already exist on the filesystem
with open('somefile', 'xt') as f:  # Throws an error if the file already exists
    f.write('Hello\n')



# Performing I/O Operations on a String
# io.StringIO class should only be used for text
import io
s = io.StringIO() #  io.StringIO('Hello\nWorld\n') this works too
s.write('Hello World\n')
print('This is a test', file=s)

s.read(10)
s.getvalue()



# Reading and Writing Compressed Datafiles
# gzip compression reading
import gzip
with gzip.open('somefile.gz', 'rt') as f:
    text = f.read()

# gzip compression writing
#  The default level is 9, which provides the highest level of compression. Lower levels offer
# better performance, but not as much compression
import gzip
with gzip.open('somefile.gz', 'wt', compresslevel=5) as f:
f.write(text)

# Layering is also allowed
import gzip
f = open('somefile.gz', 'rb')
with gzip.open(f, 'rt') as g:
    text = g.read()


# Manipulating Pathnames using os.path module
import os
path = '/Users/beazley/Data/data.csv'
# Get the last component of the path
os.path.basename(path)
# Get the directory name
os.path.dirname(path)
# Join path components together
os.path.join('tmp', 'data', os.path.basename(path))
# Expand the user's home directory
path = '~/Data/data.csv'
os.path.expanduser(path)
# Split the file extension
os.path.splitext(path)


# Testing for the Existence of a File using os.path module
import os
os.path.exists('/etc/passwd')
os.path.exists('/tmp/spam')

# TO check the type of a file/dir
# Is a regular file
os.path.isfile('/etc/passwd')
# Is a directory
os.path.isdir('/etc/passwd')
# Is a symbolic link
os.path.islink('/usr/local/bin/python3')
# Get the file linked to
os.path.realpath('/usr/local/bin/python3')

# Metadata of a file
os.path.getsize('/etc/passwd')
os.path.getmtime('/etc/passwd')
# Alternative: Get file metadata
file_metadata = [(name, os.stat(name)) for name in pyfiles]
for name, meta in file_metadata:
    print(name, meta.st_size, meta.st_mtime)


# Getting a Directory Listing using os.listdir()
import os
names = os.listdir('somedir') # Gives all files, sub dirs, links etc

import os.path
# Get all regular files
names = [name for name in os.listdir('somedir')
if os.path.isfile(os.path.join('somedir', name))]
# Get all dirs
dirnames = [name for name in os.listdir('somedir')
if os.path.isdir(os.path.join('somedir', name))]


# Serializing Python Objects
# Serialize a Python object into a byte stream so that you can do things such
# as save it to a file, store it in a database, or transmit it over a network connection

# To dump an object to a file
import pickle
data = ... # A python object
f = open('somefile', 'wb')
pickle.dump(data,f)

# To dump an object to a string
pickle.dumps(data) # dumps is dump string

# Restore from a file
f = open('somefile', 'rb')
data = pickle.load(f)
# Restore from a string
data = pickle.loads(s)


# pickle.load() should never be used on untrusted data. As a side effect
# of loading, pickle will automatically load modules and make instances.
# However, an evildoer who knows how pickle works can create “malformed”
# data that causes Python to execute arbitrary system commands.
# Thus, it’s essential that pickle only be used internally with interpreters
# that have some ability to authenticate one another.
import pickle
f = open('somedata', 'wb')
pickle.dump([1,2,3,4],f)
pickle.dump('hello', f)
pickle.dump({'Apple', 'Pear', 'Banana'}, f)

f = open('somedata', 'rb')
pickle.load(f)










