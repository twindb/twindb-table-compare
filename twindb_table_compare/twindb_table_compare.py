# -*- coding: utf-8 -*-
import string


def is_printable(str_value):
    """
    Checks if str_value is printable string
    :param str_value:
    :return: True if str_value is printable. False otherwise
    """
    return all(c in string.printable for c in str(str_value))
