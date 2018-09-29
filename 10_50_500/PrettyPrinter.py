# -*- coding: utf-8 -*-

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
        """
        error_msg = "non-empty list must be assigned ({}.unformatted_code_list)".format(self.__class__.__name__)
        try:
            assert isinstance(self.unformatted_code_list, list)
        except AssertionError as ae:
            raise TypeError(error_msg) from ae
        raise ValueError(error_msg) if not self.unformatted_code_list else False

    def format_code(self):
        """
        Formats code into blocks with an indentation style

        :param unformatted_code_list: list with code to be formatted into blocks of code
        :raises TypeError: when param is not a list
        :return: list with pretty-formatted code
        """
        self._verify_code_list()
