# -*- coding: utf-8 -*-

import re

__author__ = "mrl5"


def get_raw_code(input_string):
    """
    Removes empty lines, leading and trailing whitespaces, single and multi line comments

    :param file_path: path to .java file
    :return: list with raw code
    """
    # remove leading spaces
    line = re.sub(r'''
        ^       # start of string
        \s+     # one or more whitespaces
        ''', '', input_string, 0, re.VERBOSE)

    # remove trailing newlines
    line = line.rstrip()

    # remove '/* comments */'
    line = re.sub(r'''
        ^       # start of string
        /\*     # "/*" string
        .*      # any character (except line break) zero or more times
        \*/     # "*/" string
        \s*     # zero or many whitespaces
        ''', '', line, 0, re.VERBOSE)

    # remove '//comments'
    line = re.sub(r'''
        ^       # start of string
        //      # "//" string
        .*      # any character (except line break) zero or more times
        $       # end of string
        ''', '', line, 0, re.VERBOSE)
    return line
