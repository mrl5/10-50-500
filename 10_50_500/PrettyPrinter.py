# -*- coding: utf-8 -*-

import re

__author__ = "mrl5"


class PrettyPrinter:
    """
    Refactors Java (or other C-like languages) sourcecode with a given indentation
    """

    def __init__(self, indentation="    "):
        self.indentation = indentation
        self.unformatted_code_list = None
        self._regex_patterns = {
            "nest": "({+|^case\s+.*?:|^default\s*.*?:)",    # "{", "case x:", "default:"
            "unnest": "(}+)",                               # "}"
            "indent_break": "(\\bbreak\\b\s*;)",            # "break;"
            "line_end": ".*[{};:]$",                        # chars which end lines
            "line_break": ".*[+\-*/]$"                      # chars for breaking lines
        }
        self._brackets_nesting = 0

    def _verify_code_list(self):
        """
        :raises ValueError: if self.unformatted_code_list is empty/not assigned
        :raises TypeError: if self.unformatted_code_list is not a list
        :raises CodeWithIndentationError: if self.unformatted_code_list has lines with indentation
        """
        error_msg = "non-empty list must be assigned ({}.unformatted_code_list)".format(self.__class__.__name__)
        try:
            assert isinstance(self.unformatted_code_list, list)
        except AssertionError as ae:
            raise TypeError(error_msg) from ae
        if not self.unformatted_code_list:
            raise ValueError(error_msg)

        # list with numbers of lines with indentation
        indent_lines = [i + 1 for i, line in enumerate(self.unformatted_code_list) if re.match("^\s+", line)]
        if indent_lines:
            raise self.CodeWithIndentationError(indent_lines_list=indent_lines)

        # list with numbers of lines with trailing whitespaces
        trailing_whitespaces_lines = [i + 1 for i, line in enumerate(self.unformatted_code_list) if
                                      re.match(".*\s+$", line)]
        if trailing_whitespaces_lines:
            raise self.CodeWithTrailingWhitespacesError(trailing_whitespaces_lines_list=trailing_whitespaces_lines)

    def _get_nest_lvl(self, line, nest_lvl, line_break):
        """
        Computes nest level for sourcecode block

        :param line: line of code to analyse
        :param nest_lvl: current nest level
        :param line_break: logical value to know if line was broken (e.g. "some \n thing")
        :return: new nest level
        """
        # track {} brackets
        self._brackets_nesting += len(re.findall("{+", re.sub("[\"\'].*?[\"\']", '', line)))
        self._brackets_nesting -= len(re.findall("}+", re.sub("[\"\'].*?[\"\']", '', line)))

        # look for nesting patterns
        nest_lvl += len(re.findall(
            self._regex_patterns["nest"], re.sub(r'''   # ignore nesting characters which are inside '' or ""
                                                [\"\']  # match any single character (double quote or single quote)
                                                .*?     # any char zero or more times - "?" forces shortest matches!
                                                [\"\']  # match any single character (double quote or single quote)
                                                ''', '', line, 0, re.VERBOSE)))
        nest_lvl -= len(re.findall(self._regex_patterns["unnest"], re.sub("[\"\'].*?[\"\']", '', line)))

        # nest_lvl correction when needed
        nest_lvl += 1 if line_break else 0
        nest_lvl = self._brackets_nesting if line.endswith("}") and self._brackets_nesting != nest_lvl else nest_lvl
        return nest_lvl

    def _get_extra_indent(self, line_no, broken_line):
        """
        Provides indentation for broken lines

        :param line_no: number of line to be analysed
        :param broken_line: True if line is broken
        :return: extra indent
        """
        output = ""
        if broken_line:
            if self.unformatted_code_list[line_no].startswith(".") or \
                    re.search(self._regex_patterns["line_break"], self.unformatted_code_list[line_no - 1]):
                output = self.indentation
        return output

    def format_code(self, unformatted_code_list=None):
        """
        Formats code into blocks with an indentation style

        :param unformatted_code_list: list with code to be formatted into blocks of code
        :return: list with pretty-formatted code
        """
        self.unformatted_code_list = unformatted_code_list if unformatted_code_list is not None \
            else self.unformatted_code_list
        self._verify_code_list()
        formatted_code = []
        nest_lvl = 0
        broken_line = False
        for i, line in enumerate(self.unformatted_code_list):
            line_break = True if not re.search(self._regex_patterns["line_end"], line) else False
            indent_break = re.search(self._regex_patterns["indent_break"], re.sub("[\"\'].*?[\"\']", '', line))

            nest_lvl = self._get_nest_lvl(line, nest_lvl, line_break)
            wait_for_next_line = True if re.search(self._regex_patterns["nest"],
                                                   re.sub("[\"\'].*?[\"\']", '', line)) or line_break else False
            indent = nest_lvl * self.indentation if not wait_for_next_line else (nest_lvl - 1) * self.indentation

            # extra indent when line was broken
            indent += self._get_extra_indent(i, broken_line)
            formatted_line = indent + line
            formatted_code.append(formatted_line)

            # nest_lvl correction when needed
            nest_lvl -= 1 if indent_break else 0
            nest_lvl -= 1 if broken_line else 0
            broken_line = line_break
        return formatted_code

    class CodeWithIndentationError(Exception):
        """
        Custom exception for code with an indentation
        """

        def __init__(self, **kwargs):
            self.strerror = "Sourcecode contains lines with an indentation"
            self.indent_lines_list = kwargs["indent_lines_list"]

    class CodeWithTrailingWhitespacesError(Exception):
        """
        Custom exception for code with trailing whitespaces
        """

        def __init__(self, **kwargs):
            self.strerror = "Sourcecode contains lines with trailing whitespaces"
            self.trailing_whitespaces_lines_list = kwargs["trailing_whitespaces_lines_list"]
