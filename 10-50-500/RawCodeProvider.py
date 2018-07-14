# -*- coding: utf-8 -*-

__author__ = "mrl5"

import re


def get_raw_code(file_path):
    """
    Removes empty lines, leading and trailing whitespaces, single and multi line comments

    :param file_path: path to .java file
    :return: list with raw code
    """
    with open(file_path, "r") as f:
        raw_code = []
        multi_line_comment = False

        for line in f:
            # remove spaces from the beginning of the line and remove trailing newline
            line = re.sub(r'''
            ^       # start of string
            \s+     # one or more whitespaces
            ''', '', line, 0, re.VERBOSE).rstrip()

            # remove '/* comments */'
            line = re.sub(r'''
            ^       # start of string
            /\*     # "/*" string
            .*      # any character (except line break) zero or more times
            \*/     # "*/" string
            ''', '', line, 0, re.VERBOSE)

            # remove '//comments'
            line = re.sub(r'''
            ^       # start of string
            //      # "//" string
            .*      # any character (except line break) zero or more times
            ''', '', line, 0, re.VERBOSE)

            # remove trailing whitespaces
            line = re.sub(r'''
            \s+     # one or more whitespaces
            $       # end of string
            ''', '', line, 0, re.VERBOSE)

            # ignore empty lines
            if line != '':
                # skip multi-line comments (/*)
                if re.match(r'''
                ^       # start of string
                /       # "/" string
                \*+     # "*" string one or more times
                ''', line, re.VERBOSE):
                    multi_line_comment = True
                    continue

                # check if multi-line comment was closed (*/)
                elif re.match(r'''
                \*+     # "*" string one or more times
                /       # "/" string
                ''', line, re.VERBOSE):
                    multi_line_comment = False
                    continue

                # add line if it's not multi-line comment
                if not multi_line_comment:
                    raw_code.append(line)
    return raw_code


def pretty_print(unformatted_code_list):
    """
    Formats code into blocks with an indentation style

    :param unformatted_code_list: list with code to be formatted into blocks of code
    :return: list with pretty-formatted code
    """

    formatted_code = []
    indentation = "    "
    nest_level = 0
    wait_for_next_line = False
    # special case eg.: } catch (NullPointerException e) {
    special_case = False
    open_bracket = "{"
    close_bracket = "}"

    for line in unformatted_code_list:
        if line.endswith(open_bracket) and not line.startswith(close_bracket):
            nest_level += 1
            wait_for_next_line = True

        # case eg.: "}" or "} else"
        elif line.startswith(close_bracket) and not line.endswith(open_bracket):
            nest_level -= 1 if not special_case else 2
            wait_for_next_line = False
            special_case = False

        # case eg.: "} catch (NullPointerException e) {"
        elif line.endswith(open_bracket) and line.startswith(close_bracket):
            nest_level += 1 if not special_case else 0
            wait_for_next_line = True
            special_case = True

        formatted_code.append(nest_level * indentation + line if not wait_for_next_line
                              else (nest_level - 1) * indentation + line)
        wait_for_next_line = False

    return formatted_code


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]

    for formatted_line in pretty_print(get_raw_code(path)):
        print(formatted_line)
