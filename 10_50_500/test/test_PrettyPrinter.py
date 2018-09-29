# -*- coding: utf-8 -*-

import pytest

__author__ = "mrl5"

from PrettyPrinter import PrettyPrinter

"""
Scenario:
    - raise ValueError if 'self.unformatted_code_list' is an empty list
    - raise TypeError if 'self.unformatted_code_list' was not assigned
    - raise TypeError if 'self.unformatted_code_list' is not a list
    - 'CodeWithIndentationError' custom exception if 'self.unformatted_code_list' has items with leading whitespaces
    - "something {"
    - "}" or "} else"
    - "} catch (NullPointerException e) {"
    - compare with stripped .java file
"""


@pytest.fixture(scope="function")
def pretty_printer():
    pp = PrettyPrinter()
    return pp


def test_ValueError_when_empty_list(pretty_printer):
    pretty_printer.unformatted_code_list = []
    with pytest.raises(ValueError):
        pretty_printer.format_code()


def test_TypeError_when_field_not_assigned(pretty_printer):
    with pytest.raises(TypeError):
        pretty_printer.format_code()


def test_TypeError_when_field_not_a_list(pretty_printer):
    a_dict = {}
    pretty_printer.unformatted_code_list = a_dict
    with pytest.raises(TypeError):
        pretty_printer.format_code()


def test_CodeWithIndentationError_tabs(pretty_printer):
    input_list = []
    input_list.append("blocks")
    input_list.append("\tof")
    input_list.append("\t\tcode")
    pretty_printer.unformatted_code_list = input_list
    with pytest.raises(PrettyPrinter.CodeWithIndentationError):
        pretty_printer.format_code()


def test_CodeWithIndentationError_spaces(pretty_printer):
    input_list = []
    input_list.append("blocks")
    input_list.append("    of")
    input_list.append("        code")
    pretty_printer.unformatted_code_list = input_list
    with pytest.raises(PrettyPrinter.CodeWithIndentationError):
        pretty_printer.format_code()