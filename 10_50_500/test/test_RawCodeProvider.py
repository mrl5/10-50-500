# -*- coding: utf-8 -*-

import pytest
import os
from RawCodeProvider import get_raw_code

__author__ = "mrl5"

"""
Scenario:
1. get_raw_code
    - remove whitespaces from the beginning of the line
    - remove trailing newline
    - remove '/* comments */'
    - remove '//comments'
    - don't modify lines like "string //comment"
    - remove trailing whitespaces
    - remove empty lines
    - remove multi-line comments (/*\n\n\n*/)
    - read from file
    - return list
    
2. pretty_print
    - "something {"
    - "}" or "} else"
    - "} catch (NullPointerException e) {"
"""


@pytest.fixture(scope="function")
def directory(tmpdir):
    test_dir = tmpdir.mkdir("test_dir")
    os.mknod(os.path.join(str(test_dir), "file.txt"))
    return test_dir


def write_to_file(file, input_list):
    with open(file, 'w') as f:
        for item in input_list:
            f.write(str(item) + "\n")


def test_rm_leadnig_whitespaces(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["\tTabs versus Spaces:", "    An Eternal Holy War"]
    output_list = ["Tabs versus Spaces:", "An Eternal Holy War"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_rm_trailing_newlines(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["this is how we do it\n\n\n"]
    output_list = ["this is how we do it"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_rm_oneline_asterisk_comments(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["/* don't worry */ be happy"]
    output_list = ["be happy"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_rm_leading_doubleslash_comments(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["// you talking to me?"]
    output_list = []
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_leave_doubleslash_comments_inside_line(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["And God said, Let there be light: and there was light. // for more info check Maxwell's equations"]
    output_list = ["And God said, Let there be light: and there was light. // for more info check Maxwell's equations"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_rm_trailing_whitespaces(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["high voltage rock'n'roll        "]
    output_list = ["high voltage rock'n'roll"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_rm_multiline_comments_standard(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = []
    input_list.append("/*Takes more than combat gear to make a man")
    input_list.append("Takes more than a license for a gun")
    input_list.append("Confront your enemies, avoid them when you can*/")
    input_list.append("A gentleman will walk but never run")
    output_list = ["A gentleman will walk but never run"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_rm_multiline_comments_tricky(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = []
    input_list.append("/**")
    input_list.append('     * If "manners maketh man" as someone said')
    input_list.append("     * He's the hero of the day")
    input_list.append("     * It takes a man to suffer ignorance and smile")
    input_list.append("*/    Be yourself")
    input_list.append("no matter what they say")
    output_list = ["Be yourself", "no matter what they say"]
    write_to_file(file, input_list)
    assert get_raw_code(file) == output_list


def test_return_list(directory):
    test_dir = directory
    file = os.path.join(str(test_dir), "file.txt")
    input_list = ["test"]
    write_to_file(file, input_list)
    assert type(get_raw_code(file)) is list
