# -*- coding: utf-8 -*-

import pytest
import os
import re
from PrettyPrinter import PrettyPrinter

__author__ = "mrl5"


"""
Scenario:
    - raise ValueError if 'self.unformatted_code_list' is an empty list
    - raise TypeError if 'self.unformatted_code_list' was not assigned
    - raise TypeError if 'self.unformatted_code_list' is not a list
    - 'CodeWithIndentationError' custom exception if 'self.unformatted_code_list' has items with leading whitespaces
    - 'CodeWithTrailingWhitespacesError' custom exception if 'self.unformatted_code_list' has items with trailing whitespaces
    - 'PrettyPrinter.format_code()' method returns a list
    - "something {"
    - "}"
    - line break: "} else" or "sth.toString()
                                        .toString();"
    - "} catch (NullPointerException e) {"
    - omit { and } if inside ("" or ''
    - "case:"
    - "object.method().method().method;"
    - full .java source code
    
ToDo:
    - ugly formatted code: "}}"
    - ugly formatted code: "{{"
    - multiple brackets inside double and single quotes
"""


@pytest.fixture(scope="function")
def pretty_printer():
    pp = PrettyPrinter()
    return pp


@pytest.fixture(scope="function")
def original_java_code():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    sample_java_file = os.path.join(script_dir, "sample_java_files", "raw.java")
    with open(sample_java_file, "r") as f:
        source_code = [row.rstrip() for row in f]
    return source_code


@pytest.fixture(scope="function")
def raw_java_code(original_java_code):
    original_indentation_style = "\s{4}"
    source_code = [re.sub(original_indentation_style, '', line) for line in original_java_code]
    return source_code


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


def test_CodeWithTrailingWhitespacesError_tabs(pretty_printer):
    input_list = []
    input_list.append("blocks")
    input_list.append("of\t")
    input_list.append("code")
    pretty_printer.unformatted_code_list = input_list
    with pytest.raises(PrettyPrinter.CodeWithTrailingWhitespacesError):
        pretty_printer.format_code()


def test_CodeWithTrailingWhitespacesError_spaces(pretty_printer):
    input_list = []
    input_list.append("blocks")
    input_list.append("of ")
    input_list.append("code")
    pretty_printer.unformatted_code_list = input_list
    with pytest.raises(PrettyPrinter.CodeWithTrailingWhitespacesError):
        pretty_printer.format_code()


def test_format_code_returns_list(pretty_printer):
    pretty_printer.unformatted_code_list = ["just a test"]
    assert isinstance(pretty_printer.format_code(), list)


def test_openbracket_ending(pretty_printer, raw_java_code, original_java_code):
    pretty_printer.indentation = "    "
    stop = 4
    pretty_printer.unformatted_code_list = raw_java_code[0:stop]
    assert pretty_printer.format_code() == original_java_code[0:stop]


def test_java_code_list_given_in_method_argument(pretty_printer, raw_java_code, original_java_code):
    pretty_printer.indentation = "    "
    stop = 4
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_fourspaces_is_default_indent(pretty_printer, raw_java_code, original_java_code):
    stop = 4
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_tabbed_indent(pretty_printer):
    pretty_printer.indentation = "\t"
    flat_java_code = ["public void test() {", "nesting();"]
    tabbed_java_code = ["public void test() {", "\tnesting();"]
    assert pretty_printer.format_code(flat_java_code) == tabbed_java_code


def test_closebracket_ending(pretty_printer, raw_java_code, original_java_code):
    stop = 10
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_linebreak(pretty_printer, raw_java_code, original_java_code):
    stop = 13
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_close_and_open_brackets_in_one_line(pretty_printer, raw_java_code, original_java_code):
    stop = 17
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_brackets_inside_double_quotes(pretty_printer, raw_java_code, original_java_code):
    stop = 21
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_brackets_inside_single_quotes(pretty_printer, raw_java_code, original_java_code):
    stop = 25
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_case_indent(pretty_printer, raw_java_code, original_java_code):
    stop = 30
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_brake_indent(pretty_printer, raw_java_code, original_java_code):
    stop = 32
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_switch_case_default_break(pretty_printer, raw_java_code, original_java_code):
    stop = 34
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_real_line_break(pretty_printer, raw_java_code, original_java_code):
    stop = 38
    assert pretty_printer.format_code(raw_java_code[0:stop]) == original_java_code[0:stop]


def test_whole_file(pretty_printer, raw_java_code, original_java_code):
    stop = 38
    assert pretty_printer.format_code(raw_java_code) == original_java_code
