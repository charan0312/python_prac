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







