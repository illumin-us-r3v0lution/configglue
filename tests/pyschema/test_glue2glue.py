# -*- coding: utf-8 -*-
###############################################################################
# 
# configglue -- glue for your apps' configuration
# 
# A library for simple, DRY configuration of applications
# 
# (C) 2009--2010 by Canonical Ltd.
# originally by John R. Lenton <john.lenton@canonical.com>
# incorporating schemaconfig as configglue.pyschema
# schemaconfig originally by Ricardo Kirkner <ricardo.kirkner@canonical.com>
# 
# Released under the BSD License (see the file LICENSE)
# 
# For bug reports, support, and new releases: http://launchpad.net/configglue
# 
###############################################################################

import sys
from StringIO import StringIO

from configglue.inischema import configglue

from configglue.pyschema import ConfigSection, schemaconfigglue, options, ini2schema
from configglue.pyschema.parser import SchemaConfigParser
from configglue.pyschema.schema import Schema

import unittest

class TestGlueConvertor(unittest.TestCase):
    def setUp(self):
        # make sure we have a clean sys.argv so as not to have unexpected test
        # results
        self.old_argv = sys.argv
        sys.argv = []

    def tearDown(self):
        # restore old sys.argv
        sys.argv = self.old_argv

    def test_empty(self):
        s = ""
        _, cg, _ = configglue(StringIO(s))
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_simple(self):
        s = "[foo]\nbar = 42\n"
        _, cg, _ = configglue(StringIO(s))
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_main(self):
        s = "[__main__]\nbar = 42\n"
        _, cg, _ = configglue(StringIO(s))
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_none(self):
        s = "[__main__]\nbar = meeeeh\nbar.parser = none"
        _, cg, _ = configglue(StringIO(s),
                              extra_parsers=[('none', str)])
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_unicode(self):
        s = "[__main__]\nbar = zátrapa\nbar.parser = unicode\nbar.parser.args = utf-8"
        _, cg, _ = configglue(StringIO(s))
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_int(self):
        s = "[__main__]\nbar = 42\nbar.parser = int\n"
        _, cg, _ = configglue(StringIO(s))
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

    def test_parser_bool(self):
        s = "[__main__]\nbar = true\nbar.parser = bool \n"
        _, cg, _ = configglue(StringIO(s))
        _, sg, _ = schemaconfigglue(ini2schema(StringIO(s)))
        self.assertEqual(vars(cg), vars(sg))

if __name__ == '__main__':

    unittest.main()
