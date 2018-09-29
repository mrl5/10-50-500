# -*- coding: utf-8 -*-

__author__ = "mrl5"


def pretty_print(unformatted_code_list):
    """
    Formats code into blocks with an indentation style

    :param unformatted_code_list: list with code to be formatted into blocks of code
    :raises TypeError: when param is not a list
    :return: list with pretty-formatted code
    """
    # check if param is a list
    try:
        assert unformatted_code_list == list()
    except AssertionError:
        raise TypeError
