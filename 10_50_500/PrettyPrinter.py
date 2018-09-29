# -*- coding: utf-8 -*-

import re

__author__ = "mrl5"


class PrettyPrinter:
    """
    Print Java (or other C-like languages) sourcecode with a given indentation
    """

    def __init__(self, indentation="    "):
        self.indentation = indentation
        self.unformatted_code_list = None

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
        indent_lines = [i + 1 if re.match("^\s+", line) else None for i, line in enumerate(self.unformatted_code_list)]
        # list with elements which are not equal to None
        indent_lines = list(filter(None.__ne__, indent_lines))
        if indent_lines:
            raise self.CodeWithIndentationError(indent_lines_list=indent_lines)
        # list with numbers of lines with trailing whitespaces
        trailing_whitespaces_lines = [i + 1 if re.match(".*\s+$", line) else None for i, line in
                                      enumerate(self.unformatted_code_list)]
        trailing_whitespaces_lines = list(filter(None.__ne__, trailing_whitespaces_lines))
        if trailing_whitespaces_lines:
            raise self.CodeWithTrailingWhitespacesError(trailing_whitespaces_lines_list=trailing_whitespaces_lines)

    def format_code(self):
        """
        Formats code into blocks with an indentation style

        :param unformatted_code_list: list with code to be formatted into blocks of code
        :return: list with pretty-formatted code
        """
        self._verify_code_list()
        formatted_code = []
        nest_lvl = 0
        end_of_line_break = False
        # "{" or "case sth:"
        nest_regex_pattern = "({|\s*case\s+.*?:\s*$)"
        # "}" or "break;"
        unnest_regex_pattern = "(\}|\s*break;)"
        for row in self.unformatted_code_list:
            line = str(row)
            # if line doesn't end with "{" or "}" or ";" then it's line break
            line_break = True if not re.search(".*[{};:]$", line) else False
            wait_for_next_line = True if re.search(nest_regex_pattern,
                                                   re.sub("[\"\'].*?[\"\']", '', line)) or line_break else False

            # find all characters which make nesting, but are not inside '' or ""
            nest_lvl += len(re.findall(nest_regex_pattern, re.sub(r'''
                                                    [\"\']  # match any single character (double quote or single quote)
                                                    .*?     # any char zero or more times - "?" forces shortest matches!
                                                    [\"\']  # match any single character (double quote or single quote)
                                                    ''', '', line, 0, re.VERBOSE)))
            nest_lvl -= len(re.findall(unnest_regex_pattern, re.sub("[\"\'].*?[\"\']", '', line)))
            # add nesting on line break
            nest_lvl += 1 if line_break else 0

            # add new line with an indentation
            indent = nest_lvl * self.indentation if not wait_for_next_line else (nest_lvl - 1) * self.indentation
            formatted_line = indent + line
            formatted_code.append(formatted_line)
            # retrieve normal nest level
            nest_lvl -= 1 if end_of_line_break else 0
            end_of_line_break = line_break
            # debug
            print(formatted_line)
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
