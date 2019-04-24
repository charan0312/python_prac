# -*- coding: utf-8 -*-

# Split a string when the delimiters are not consistent
line = 'asdf fjdk; afed, fjek,asdf,     foo'

# Use re.split() to have more control
import re
re.split(r'[;,\s]\s*', line)

# Be careful if the regex contains capture group enclosed in parentheses. If capture groups are used,
# then the matched text is also included in the result.
fields = re.split(r'(;|,|\s)\s*', line)
fields

# To get back the string by joining the split string with delimiters
values = fields[::2]
delimiters = fields[1::2] + ['']

values
delimiters

# Reforming the string
''.join(v + d for v,d in zip(values,delimiters))


# Basic prefix/suffix checking - use startswith() or endswith() with str or tuple as input
filename = 'spam.txt'
filename.endswith('.txt')
filename.startswith('file:')

# For mutiple choices use a tuple of choices
import os
filenames = os.listdir('.')
filenames

[f for f in filenames if f.endswith(('.py','.txt'))]

# Using siles is clumsy and using regex is a bit of overkill
import re
url = 'http://www.python.org'
if re.match(r'http:|https:|ftp:', url):
    print('abcd')


# Matching and Searching for text patterns
# For simple literals we can use str.find(), str.startswith() or str.endswith() 
text = 'yeah, but no, but yeah, but no, but yeah'
text.find('yeah') # returns the location of first occurence

# For complicated matchings we can use re module
text1 = '11/27/2012uyhg'

import re
if re.match(r'\d+/\d+/\d+', text1):  # \d+ matches for one or more digits
    print('yes')
else:
    print('no')


# If we are performing matching using same pattern many times
# Use re.compile() to precompile the pattern
date_pattern =  re.compile(r'\d+/\d+/\d+$')

# match only checks the beginning of the string. If we want exact match use '$' at the end of pattern
if date_pattern.match(text1):    
    print('yes')
else:
    print('no')
 
if date_pattern.findall(text1):    
    print('yes')
else:
    print('no')    

    
# TO find all the matches use re.findall()
# The findall() method searches the text and finds all matches, returning them as a list.
# If you want to find matches iteratively, use the finditer()
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
re.findall(date_pattern, text)
date_pattern.findall(text)


# Capture groups in re are useful for subsequent processing of matched text
# The contents of each group can be extracted individually
# if we are not using a raw string for matching we'll have to escape the '\'
date_pattern =  re.compile(r'(\d+)/(\d+)/(\d+)')  
m = date_pattern.match('3/13/2013cv1')
m.groups()
m.group(0)
m.group(1)


# Search and Replace a text pattern using str.replace() and re.sub()
text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'
text.replace('Today', 'today')

# For complicated patterns use re.sub() and also a substitution callback function
import re
re.sub(r'(\d+)/(\d+)/(\d+)', r'\3-\1-\2', text) # \3 is a capture group

date_pattern =  re.compile(r'(\d+)/(\d+)/(\d+)')  
date_pattern.sub(r'\3-\1-\2', text)

from calendar import month_name
def change_date(m):
    mon_name = month_name[int(m.group(1))]
    return '{} {} {}'.format(m.group(2), mon_name, m.group(3))

date_pattern.sub(change_date, text)
new_text, n = date_pattern.subn(change_date, text) # n gives no of subs
n


# To do case-insensitive text operations use flags in re module
text = 'UPPER PYTHON, lower python, Mixed Python'
re.findall('python', text) # case sensitive
re.findall('python', text, flags=re.IGNORECASE)

re.sub('python', 'snake', text, flags=re.IGNORECASE) # This doesn't match the case of replaced text

def matchcase(word):
    def replace(m):
        text = m.group()
        if text.isupper():
            return word.upper()
        elif text.islower():
            return word.lower()
        elif text[0].isupper():
            return word.capitalize()
        else:
            return word
    return replace

# Using a support function will help in matching the case
re.sub('python', matchcase('snake'), text, flags=re.IGNORECASE)


# '*' in regex matches greedily and if you want to match in a non-greedy fashion use '?' after '*'
text2 = 'Computer says "no." Phone says "yes."'
re.findall(r'\"(.*)\"', text2) # gives longest possible match
str_pat = re.compile(r'\"(.*?)\"') # gives shortest possible match
str_pat.findall(text2)

# To add support for matching the newline character for '.'
text2 = '''/* this is a
multiline comment */'''
# (?:.|\n) specifies a noncapture group (i.e., it defines a group for the
# purposes of matching, but that group is not captured separately or numbered)
comment = re.compile(r'/\*((?:.|\n)*?)\*/')
comment.findall(text2)

# re.DOTALL can be used for this purpose but only for simple matchings
comment = re.compile(r'/\*(.*?)\*/', re.DOTALL) # If possible avoid using flags
comment.findall(text2)


# To make sure that all of the Unicode strings have the same underlying representation.
s1 = 'Spicy Jalape\u00f1o'
s2 = 'Spicy Jalapen\u0303o'
print(s1,len(s1))
print(s2,len(s2))
s1 == s2 # “Spicy Jalapeño” has 2 representations and both are not the same

# TO fix this we should first normalize the string using unicodedata module
import unicodedata
t1 = unicodedata.normalize('NFC', s1) # fully composed
t2 = unicodedata.normalize('NFC', s2)
t1 == t2
print(ascii(t1), ascii(t2))

t3 = unicodedata.normalize('NFD', s1) # fully decomposed
t4 = unicodedata.normalize('NFD', s2)
t3 == t4
print(ascii(t3), ascii(t4))

# Remove all diacritical marks from the text for sanitizing and filtering
t1 = unicodedata.normalize('NFD', s1)
''.join(c for c in t1 if not unicodedata.combining(c)) # combining() tests characters against character class


# Stripping unwanted characters from strings, strip() is used to strip from beginning or end of a string
# Using lstrip and rstrip by default strips leading or trailing spaces
# But we can specify the character to be stripped
t = '-----hello====='
t.rstrip('=')
t.lstrip('-') 
t.strip('=-')

# We cannot strip at the middle of a string
s = ' hello                 world \n'
s.strip()
# Use regex or replace for inner characters
s.replace(' ', '')

import re
re.sub(r'\s+', ' ', s)


# Sanitizing and Cleaning Up Text
s = 'pýtĥöñ\fis\tawesome\r\n'

# For simple replacement str.replace() is better and for any non trivial character to character remapping or deletion use translate()
# for translate we give a dictionary as input
remap = {ord('\t') : ' ',
ord('\f') : ' ',
ord('\r') : None # Deleted
}
a = s.translate(remap)
a

# We can extend this further by removing all the combining characters
import unicodedata
import sys
# We are creating a dictionary of combining chars as keys and NONE as values
cmd_chars = dict.fromkeys(c for c in range(sys.maxunicode) if unicodedata.combining(chr(c)))
# First we decompose the combining chars and then translate
b = unicodedata.normalize('NFD', a)
b
b.translate(cmd_chars)

# for digits
digitmap = { c: ord('0') + unicodedata.digit(chr(c)) for c in range(sys.maxunicode) if unicodedata.category(chr(c)) == 'Nd' }
len(digitmap)
x = '\u0661\u0662\u0663'
x
x.translate(digitmap)


# I/O decoding and encoding to strip or alter the data. Onlly if getting the text in ASCII format is the final goal
a
b = unicodedata.normalize('NFD', a)
b.encode('ascii', 'ignore').decode('ascii')


# Aligning strings: ljust(), rjust(), center()
text = 'Hello World'
text.ljust(20) # 20 is the len of the final string
text.rjust(20, '*')
text.center(20)

# Format can also be used for aligning strings using >,<,^ for rjust, ljust, center respectively
format(text, '>20')
format(text, '+>20s')# for fillina +

'{:>10.2s} {:>10.2s}'.format('Hello', 'World')

'{:3.2f}, {:20.10f}'.format(100.345678, 100.0)


# Combining and Concatenating Strings
# Fastest way is to use join()
# Using + for concatenating a lot of string is very inefficient
parts = ['Is', 'Chicago', 'Not', 'Chicago?']
" ".join(str(p) for p in parts) # Using generator is more efficient

# use print's capability 
print('a', 'b', 'c', sep=':')

# if you’re writing code that is building output from lots of small strings,
# you might consider writing that code as a generator function, using yield to emit fragments.
def sample():
    yield 'Is'
    yield 'Chicago'
    yield 'Not'
    yield 'Chicago?'

# Smart method about combining I/O operations based on a maxsize
# Version 1 (string concatenation)
f.write(chunk1 + chunk2) # Better when chunk1 and chunk2 are small
# Version 2 (separate I/O operations)
f.write(chunk1) # Better when chunk1 and chunk2 are big
f.write(chunk2)

def combine(source, maxsize):
    parts = []
    size = 0
    for part in source:
        parts.append(part)
        size += len(part)
        if size > maxsize:
            yield ''.join(parts)
            parts = []
            size = 0
    yield ''.join(parts)
for part in combine(sample(),32768):
    f.write(part)


# Interpolating Variables in Strings
s = '{name} has {n} messages.'
s.format(name='hello', n=10) # format_map can also be used


# Reformatting Text to a Fixed Number of Columns
# textwrap module can be used
s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
the eyes, not around the eyes, don't look around the eyes, \
look into my eyes, you're under."

import textwrap
print(textwrap.fill(s,60))
print(textwrap.fill(s,30, initial_indent='    '))
print(textwrap.fill(s,30, subsequent_indent='    '))


# 







