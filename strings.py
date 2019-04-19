# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 01:03:50 2019

@author: chara
"""

# Split a string when the delimiters are not consistent

line = 'asdf fjdk; afed, fjek,asdf,     foo'

# Use re.split() to have more control
import re
re.split(r'[;,\s]\s*', line)

# Be careful if the regex contains capture group enclosed in parentheses. If capture groups are used,
# then the matched text is also included in the result.
fields = re.split(r'(;|,|\s)\s*', line)
fields
