# -*- coding: utf-8 -*-


__author__ = "mrl5"

"""
Scenario:
A. get_raw_code
    1. Handle exceptions from 'with open()'
    2. Remove spaces from the beginning of the line and remove trailing newline
    3. Remove '/* comments */'
    4. Remove '//comments'
    5. Remove trailing whitespaces
    6. Remove multi-line comments (/*\n\n\n*/)
    
B. pretty_print
    1. "something {"
    2. "}" or "} else"
    3. "} catch (NullPointerException e) {"
"""

