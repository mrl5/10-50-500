# -*- coding: utf-8 -*-

import pytest
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
    - ugly formatted code: "}}"
    - ugly formatted code: "{{"
    - omit { and } if inside ("" or ''
    - "} catch (NullPointerException e) {"
    - "case:"
    - "object.method().method().method;"
    - compare with stripped .java file
"""


@pytest.fixture(scope="function")
def pretty_printer():
    pp = PrettyPrinter()
    return pp


@pytest.fixture(scope="function")
def raw_java_code():
    source_code = []
    source_code.append("package com.tuxnet.utils;")
    source_code.append("public class Test {")
    source_code.append("public static void main(String[] args) {")
    source_code.append("Bash bash = new Bash();")
    source_code.append("Integer test = 0;")
    source_code.append("if (true) {")
    source_code.append("for (String line : bash.verboseCmd(\"ls -la\")) {")
    source_code.append("System.out.println(line);")
    source_code.append("}")
    source_code.append("} else")
    source_code.append("System.out.println(\"false\");")
    source_code.append("bash.quiet(\"uname -a\");")
    source_code.append("try {")
    source_code.append("bash.quiet(\"ping www.github.com\");")
    source_code.append("} catch (NullPointerException e) {")
    source_code.append("System.err.println(\"we are doomed\");")
    source_code.append("}")
    source_code.append("switch (test) {")
    source_code.append("case 0:")
    source_code.append("boolean worked = test.toString()")
    source_code.append(".endsWith(\"1\");")
    source_code.append("break;")
    source_code.append("case 1:")
    source_code.append("String s = test.toString();")
    source_code.append("break;")
    source_code.append("}")
    source_code.append("}")
    source_code.append("}")
    return source_code


@pytest.fixture(scope="function")
def tabbed_java_code():
    source_code = []
    source_code.append("package com.tuxnet.utils;")
    source_code.append("public class Test {")
    source_code.append("\tpublic static void main(String[] args) {")
    source_code.append("\t\tBash bash = new Bash();")
    source_code.append("\t\tInteger test = 0;")
    source_code.append("\t\tif (true) {")
    source_code.append("\t\t\tfor (String line : bash.verboseCmd(\"ls -la\")) {")
    source_code.append("\t\t\t\tSystem.out.println(line);")
    source_code.append("\t\t\t}")
    source_code.append("\t\t} else")
    source_code.append("\t\t\tSystem.out.println(\"false\");")
    source_code.append("\t\tbash.quiet(\"uname -a\");")
    source_code.append("\t\ttry {")
    source_code.append("\t\t\tbash.quiet(\"ping www.github.com\");")
    source_code.append("\t\t} catch (NullPointerException e) {")
    source_code.append("\t\t\tSystem.err.println(\"we are doomed\");")
    source_code.append("\t\t}")
    source_code.append("\t\tswitch (test) {")
    source_code.append("\t\t\tcase 0:")
    source_code.append("\t\t\t\tboolean worked = test.toString()")
    source_code.append("\t\t\t\t\t\t.endsWith(\"1\");")
    source_code.append("\t\t\t\tbreak;")
    source_code.append("\t\t\tcase 1:")
    source_code.append("\t\t\t\tString s = test.toString();")
    source_code.append("\t\t\t\tbreak;")
    source_code.append("\t\t}")
    source_code.append("\t}")
    source_code.append("}")
    return source_code


@pytest.fixture(scope="function")
def fourspaced_java_code():
    source_code = []
    source_code.append("package com.tuxnet.utils;")
    source_code.append("public class Test {")
    source_code.append("    public static void main(String[] args) {")
    source_code.append("        Bash bash = new Bash();")
    source_code.append("        Integer test = 0;")
    source_code.append("        if (true) {")
    source_code.append("            for (String line : bash.verboseCmd(\"ls -la\")) {")
    source_code.append("                System.out.println(line);")
    source_code.append("            }")
    source_code.append("        } else")
    source_code.append("            System.out.println(\"false\");")
    source_code.append("        bash.quiet(\"uname -a\");")
    source_code.append("        try {")
    source_code.append("            bash.quiet(\"ping www.github.com\");")
    source_code.append("        } catch (NullPointerException e) {")
    source_code.append("            System.err.println(\"we are doomed\");")
    source_code.append("        }")
    source_code.append("        switch (test) {")
    source_code.append("            case 0:")
    source_code.append("                boolean worked = test.toString()")
    source_code.append("                        .endsWith(\"1\");")
    source_code.append("                break;")
    source_code.append("            case 1:")
    source_code.append("                String s = test.toString();")
    source_code.append("                break;")
    source_code.append("        }")
    source_code.append("    }")
    source_code.append("}")
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


def test_openbracket_ending(pretty_printer, raw_java_code, tabbed_java_code):
    pretty_printer.indentation = "\t"
    start = 0
    stop = 3
    raw_java_code = raw_java_code[start:stop]
    tabbed_java_code = tabbed_java_code[start:stop]
    pretty_printer.unformatted_code_list = raw_java_code
    assert pretty_printer.format_code() == tabbed_java_code


def test_closebracket_ending(pretty_printer, raw_java_code, tabbed_java_code):
    pretty_printer.indentation = "\t"
    start = 0
    stop = 10
    raw_java_code = raw_java_code[start:stop]
    tabbed_java_code = tabbed_java_code[start:stop]
    pretty_printer.unformatted_code_list = raw_java_code
    assert pretty_printer.format_code() == tabbed_java_code


def test_linebreak(pretty_printer, raw_java_code, tabbed_java_code):
    pretty_printer.indentation = "\t"
    start = 0
    stop = 12
    raw_java_code = raw_java_code[start:stop]
    tabbed_java_code = tabbed_java_code[start:stop]
    pretty_printer.unformatted_code_list = raw_java_code
    assert pretty_printer.format_code() == tabbed_java_code


@pytest.mark.skip
def test_fourspaced_indent(pretty_printer, raw_java_code, fourspaced_java_code):
    pretty_printer.indentation = "    "
    assert pretty_printer.format_code(raw_java_code) == fourspaced_java_code


@pytest.mark.skip
def test_tabbed_indent(pretty_printer, raw_java_code, tabbed_java_code):
    pretty_printer.indentation = "\t"
    assert pretty_printer.format_code(raw_java_code) == tabbed_java_code
