# -*- coding: utf-8 -*-

import re

__author__ = "mrl5"


def get_raw_code(input_string):
    """
    Removes empty lines, leading and trailing whitespaces, single and multi line comments

    :param file_path: path to .java file
    :return: list with raw code
    """
    line = re.sub(r'''
        ^   # start of string
        \s+ # one or more whitespaces
        ''', '', input_string, 0, re.VERBOSE)
    return line
