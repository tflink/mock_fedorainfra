#
# conftest.py - utils for py.test
#
# Copyright 2011, Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Author: Tim Flink <tflink@redhat.com>

import pytest
import re

def pytest_addoption(parser):
    """
    Add an option to the py.test parser to detect when the functional tests
    should be detected and run
    """

    parser.addoption('--functional', action='store_true', default=False,
                    help='Add functional tests')

def pytest_ignore_collect(path, config):
    """Prevents collection of any files named testfunc* to speed up non
        integration tests"""
    if path.fnmatch('*testfunc*'):
        try:
            is_functional = config.getvalue('functional')
        except KeyError:
            return True

        return not is_functional

def pytest_configure(config):
    """This is a bit of a hack to detect whether or not we are running inside
        a test environment"""
    import sys
    sys._called_from_test = True
