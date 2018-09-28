# -*- coding: utf-8 -*-

import pytest
import os
from RawCodeProvider import get_raw_code

__author__ = "mrl5"

"""
Scenario:
A. get_raw_code
    1. Remove spaces from the beginning of the line and remove trailing newline
    2. Remove '/* comments */'
    3. Remove '//comments'
    4. Remove trailing whitespaces
    5. Remove multi-line comments (/*\n\n\n*/)
    6. Read from file
    7. Return list with raw code
    
B. pretty_print
    1. "something {"
    2. "}" or "} else"
    3. "} catch (NullPointerException e) {"
"""


def test_rm_leadnig_spaces():
    input_string = "    never ending story"
    return_string = "never ending story"
    assert get_raw_code(input_string) == return_string
