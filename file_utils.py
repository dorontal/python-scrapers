#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017 Doron Tal
"""
file_utils - io from file files w/multiple objects
"""

import unittest

BUFFER_SIZE = 64*1024

class ReverseFileIterator(object):
    """
    Class containing some file utilities as methods
    """
    def __init__(self, s_filename):
        """
        setup
        """
        self._h_file = open(s_filename, "r")
        self._h_file.seek(0, 2)
        self._position = self._h_file.tell()
        self._leftover = None
        self._l_lines = []

    def __iter__(self):
        """
        part of allowing this class's objects to also be used as iterators
        """
        return self

    def _read_next_batch(self):
        """
        this object is made an iterator for going through freebase results
        """
        if self._position > 0:
            assert len(self._l_lines) == 0
            size = min(self._position, BUFFER_SIZE)
            self._position -= size
            self._h_file.seek(self._position)
            s_buffer = self._h_file.read(size)
            self._l_lines = s_buffer.split("\n")
            del s_buffer
            if self._leftover is not None:
                self._l_lines[-1] = self._l_lines[-1]+self._leftover
            elif not self._l_lines[-1]:
                # self._leftover is None and not l_lines[-1]
                del self._l_lines[-1]
            # update leftovers
            if self._position > 0:
                self._leftover = self._l_lines[0]
                del self._l_lines[0]
            else:
                self._leftover = None
        else:
            raise StopIteration

    def next(self):
        """
        next..
        """
        if len(self._l_lines) == 0:
            self._read_next_batch()

        assert len(self._l_lines) > 0
        return self._l_lines.pop()

    def all(self):
        """
        runs next() over and over until the end
        """
        return [i for i in self]

class ModuleTests(unittest.TestCase):
    """
    module tests
    """
    @staticmethod
    def test_basic():
        """
        tests
        """
        s_filename = "/etc/passwd"
        for s_line in ReverseFileIterator(s_filename):
            print s_line


if __name__ == '__main__':
    unittest.main()
