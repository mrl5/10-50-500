# -*- coding: utf-8 -*-

import pytest
import os
from RawCodeProvider import get_raw_code

__author__ = "mrl5"

"""
Scenario:
1. get_raw_code
    - remove spaces from the beginning of the line
    - remove trailing newline
    - remove '/* comments */'
    - remove '//comments'
    - remove trailing whitespaces
    - remove multi-line comments (/*\n\n\n*/)
    - read from file
    - return list with raw code
    
2. pretty_print
    - "something {"
    - "}" or "} else"
    - "} catch (NullPointerException e) {"
"""


def test_rm_leadnig_spaces():
    input_string = "    never ending story"
    output_string = "never ending story"
    assert get_raw_code(input_string) == output_string


def test_rm_trailing_newline():
    input_string = "this is how we do it\n\n\n"
    output_string = "this is how we do it"
    assert get_raw_code(input_string) == output_string
