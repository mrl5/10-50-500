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

    def format_code(self):
        """
        Formats code into blocks with an indentation style

        :param unformatted_code_list: list with code to be formatted into blocks of code
        :return: list with pretty-formatted code
        """
        self._verify_code_list()

    class CodeWithIndentationError(Exception):
        """
        Custom exception for code with an indentation
        """
        def __init__(self, **kwargs):
            self.strerror = "Sourcecode contains lines with an indentation"
            self.indent_lines_list = kwargs["indent_lines_list"]
