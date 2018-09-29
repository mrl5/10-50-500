# -*- coding: utf-8 -*-

import pytest

__author__ = "mrl5"

from PrettyPrinter import pretty_print

"""
Scenario:
    - test if param is list
    - "something {"
    - "}" or "} else"
    - "} catch (NullPointerException e) {"
    - compare with stripped .java file
"""


def test_exception_when_param_not_list():
    a_dict = {}
    with pytest.raises(TypeError):
        pretty_print(a_dict)
