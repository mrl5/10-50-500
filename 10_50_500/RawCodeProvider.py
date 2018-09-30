# -*- coding: utf-8 -*-

import re

__author__ = "mrl5"


def get_raw_code(file_path):
    """
    Removes empty lines, leading and trailing whitespaces, single and multi line comments

    :param file_path: path to .java file
    :return: list with raw code
    """
    raw_code = []
    multi_line_comment = False
    with open(file_path, "r") as f:
        for row in f:
            # remove leading and trailing whitespaces
            line = row.strip()

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

            # ignore empty lines
            if line != '':
                # skip multi-line comments (/*)
                if re.search(r'''
                        ^       # start of string
                        /\*     # "/*" string
                        .*      # any character (except line break) zero or more times
                        ''', line, re.VERBOSE):
                    multi_line_comment = True
                    continue
                # check if multi-line comment was closed (*/)
                elif re.search(r'''
                        .*      # any character (except line break) zero or more times
                        \*/     # "*/" string
                        $       # end of string
                        ''', line, re.VERBOSE):
                    multi_line_comment = False
                    line = re.sub(r'''
                        .*      # any character (except line break) zero or more times
                        \*/     # "*/" string
                        \s*     # zero or many whitespaces
                        ''', '', line, 0, re.VERBOSE)
                    if line == '':
                        continue
                # add line if it's not multi-line comment
                if not multi_line_comment:
                    raw_code.append(line)
    return raw_code


def main():
    path = sys.argv[1] if (sys.argv[0] == __file__) else sys.argv[0]
    pp = PrettyPrinter()
    for formatted_line in pp.format_code(get_raw_code(path)):
        print(formatted_line)


if __name__ == "__main__":
    import sys
    from PrettyPrinter import PrettyPrinter
    main()
