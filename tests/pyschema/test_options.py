# Copyright 2010 Canonical Ltd.  This software is licensed under the
# GNU Lesser General Public License version 3 (see the file LICENSE).

import unittest
from StringIO import StringIO

from configglue.pyschema.options import (BoolConfigOption, IntConfigOption,
    StringConfigOption, LinesConfigOption, TupleConfigOption, DictConfigOption)
from configglue.pyschema.parser import SchemaConfigParser
from configglue.pyschema.schema import Schema


class TestStringConfigOption(unittest.TestCase):
    def test_init_no_args(self):
        opt = StringConfigOption()
        self.assertFalse(opt.null)

    def test_init_null(self):
        opt = StringConfigOption(null=True)
        self.assertTrue(opt.null)

    def test_parse_string(self):
        class MySchema(Schema):
            foo = StringConfigOption(null=True)
        config = StringIO("[__main__]\nfoo = 42")
        expected_values = {'__main__': {'foo': '42'}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        config = StringIO("[__main__]\nfoo = ")
        expected_values = {'__main__': {'foo': ''}}
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        config = StringIO("[__main__]\nfoo = None")
        expected_values = {'__main__': {'foo': None}}
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        class MySchema(Schema):
            foo = StringConfigOption()
        config = StringIO("[__main__]\nfoo = None")
        expected_values = {'__main__': {'foo': 'None'}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_default(self):
        opt = StringConfigOption()
        self.assertEqual(opt.default, '')

    def test_default_null(self):
        opt = StringConfigOption(null=True)
        self.assertEqual(opt.default, None)


class TestIntConfigOption(unittest.TestCase):
    def test_parse_int(self):
        class MySchema(Schema):
            foo = IntConfigOption()
        config = StringIO("[__main__]\nfoo = 42")
        expected_values = {'__main__': {'foo': 42}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        config = StringIO("[__main__]\nfoo =")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

        config = StringIO("[__main__]\nfoo = bla")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

    def test_default(self):
        opt = IntConfigOption()
        self.assertEqual(opt.default, 0)


class TestBoolConfigOption(unittest.TestCase):
    def test_parse_bool(self):
        class MySchema(Schema):
            foo = BoolConfigOption()
        config = StringIO("[__main__]\nfoo = Yes")
        expected_values = {'__main__': {'foo': True}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        config = StringIO("[__main__]\nfoo = tRuE")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        config = StringIO("[__main__]\nfoo =")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

        config = StringIO("[__main__]\nfoo = bla")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

    def test_default(self):
        opt = BoolConfigOption()
        self.assertEqual(opt.default, False)


class TestLinesConfigOption(unittest.TestCase):
    def test_parse_int_lines(self):
        class MySchema(Schema):
            foo = LinesConfigOption(item=IntConfigOption())

        config = StringIO("[__main__]\nfoo = 42\n 43\n 44")
        expected_values = {'__main__': {'foo': [42, 43, 44]}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_bool_lines(self):
        class MySchema(Schema):
            foo = LinesConfigOption(item=BoolConfigOption())
        schema = MySchema()
        config = StringIO("[__main__]\nfoo = tRuE\n No\n 0\n 1")
        expected_values = {'__main__': {'foo': [True, False, False, True]}}
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(expected_values, parser.values())

    def test_parse_bool_empty_lines(self):
        class MySchema(Schema):
            foo = LinesConfigOption(item=BoolConfigOption())
        schema = MySchema()
        config = StringIO("[__main__]\nfoo =")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        expected_values = {'__main__': {'foo': []}}
        self.assertEqual(expected_values, parser.values())

    def test_parse_bool_invalid_lines(self):
        class MySchema(Schema):
            foo = LinesConfigOption(item=BoolConfigOption())
        schema = MySchema()
        config = StringIO("[__main__]\nfoo = bla")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

        config = StringIO("[__main__]\nfoo = True\n bla")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

    def test_default(self):
        opt = LinesConfigOption(item=IntConfigOption())
        self.assertEqual(opt.default, [])

    def test_remove_duplicates(self):
        class MySchema(Schema):
            foo = LinesConfigOption(item=StringConfigOption(),
                                    remove_duplicates=True)
        schema = MySchema()
        config = StringIO("[__main__]\nfoo = bla\n blah\n bla")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEquals({'__main__': {'foo': ['bla', 'blah']}},
                          parser.values())

    def test_remove_dict_duplicates(self):
        class MyOtherSchema(Schema):
            foo = LinesConfigOption(item=DictConfigOption(),
                                    remove_duplicates=True)
        schema = MyOtherSchema()
        config = StringIO("[__main__]\nfoo = bla\n bla\n[bla]\nbar = baz")
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEquals({'__main__': {'foo': [{'bar': 'baz'}]}},
                          parser.values())

class TestTupleConfigOption(unittest.TestCase):
    def test_init(self):
        opt = TupleConfigOption(2)
        self.assertEqual(opt.length, 2)

    def test_init_no_length(self):
        opt = TupleConfigOption()
        self.assertEqual(opt.length, 0)
        self.assertEqual(opt.default, ())

    def test_parse_no_length(self):
        class MySchema(Schema):
            foo = TupleConfigOption()

        config = StringIO('[__main__]\nfoo=1,2,3,4')
        expected_values = {'__main__': {'foo': ('1', '2', '3', '4')}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_tuple(self):
        class MySchema(Schema):
            foo = TupleConfigOption(length=4)
        config = StringIO('[__main__]\nfoo = 1, 2, 3, 4')
        expected_values = {'__main__': {'foo': ('1', '2', '3', '4')}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

        config = StringIO('[__main__]\nfoo = 1, 2, 3')
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

        config = StringIO('[__main__]\nfoo = ')
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertRaises(ValueError, parser.values)

    def test_default(self):
        opt = TupleConfigOption(2)
        self.assertEqual(opt.default, ())


class TestDictConfigOption(unittest.TestCase):
    def test_init(self):
        opt = DictConfigOption()
        self.assertEqual(opt.spec, {})
        self.assertEqual(opt.strict, False)

        spec = {'a': IntConfigOption(), 'b': BoolConfigOption()}
        opt = DictConfigOption(spec)
        self.assertEqual(opt.spec, spec)
        self.assertEqual(opt.strict, False)

        opt = DictConfigOption(spec, strict=True)
        self.assertEqual(opt.spec, spec)
        self.assertEqual(opt.strict, True)

    def test_get_extra_sections(self):
        class MySchema(Schema):
            foo = DictConfigOption(item=DictConfigOption())

        config = StringIO("""
[__main__]
foo=dict1
[dict1]
bar=dict2
[dict2]
baz=42
""")
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        expected = ['dict2']

        opt = DictConfigOption(item=DictConfigOption())
        extra = opt.get_extra_sections('dict1', parser)
        self.assertEqual(extra, expected)

    def test_parse_dict(self):
        class MySchema(Schema):
            foo = DictConfigOption({'bar': StringConfigOption(),
                                    'baz': IntConfigOption(),
                                    'bla': BoolConfigOption(),
                                    })
        config = StringIO("""[__main__]
foo = mydict
[mydict]
bar=baz
baz=42
bla=Yes
""")
        expected_values = {
            '__main__': {
                'foo': {'bar': 'baz', 'baz': 42, 'bla': True}
            }
        }

        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_raw(self):
        class MySchema(Schema):
            foo = DictConfigOption({'bar': StringConfigOption(),
                                    'baz': IntConfigOption(),
                                    'bla': BoolConfigOption(),
                                    })
        config = StringIO("""[__main__]
foo = mydict
[mydict]
baz=42
""")
        expected = {'bar': '', 'baz': '42', 'bla': 'False'}

        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        parsed = schema.foo.parse('mydict', parser, True)
        self.assertEqual(parsed, expected)

    def test_parse_invalid_key_in_parsed(self):
        class MySchema(Schema):
            foo = DictConfigOption({'bar': IntConfigOption()})

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]\nbaz=2")
        expected_values = {'__main__': {'foo': {'bar': 0, 'baz': '2'}}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_invalid_key_in_spec(self):
        class MySchema(Schema):
            foo = DictConfigOption({'bar': IntConfigOption(),
                                    'baz': IntConfigOption(fatal=True)})

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]\nbar=2")
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertRaises(ValueError, parser.parse_all)

    def test_default(self):
        opt = DictConfigOption({})
        self.assertEqual(opt.default, {})

    def test_parse_no_strict_missing_args(self):
        class MySchema(Schema):
            foo = DictConfigOption({'bar': IntConfigOption()})

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]")
        expected_values = {'__main__': {'foo': {'bar': 0}}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_no_strict_extra_args(self):
        class MySchema(Schema):
            foo = DictConfigOption()

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]\nbar=2")
        expected_values = {'__main__': {'foo': {'bar': '2'}}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_no_strict_with_item(self):
        class MySchema(Schema):
            foo = DictConfigOption(
                      item=DictConfigOption(
                          item=IntConfigOption()))
        config = StringIO("""
[__main__]
foo = mydict
[mydict]
bar = baz
[baz]
wham=42
""")
        expected_values = {'__main__': {'foo': {'bar': {'wham': 42}}}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_strict(self):
        class MySchema(Schema):
            spec = {'bar': IntConfigOption()}
            foo = DictConfigOption(spec, strict=True)

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]\nbar=2")
        expected_values = {'__main__': {'foo': {'bar': 2}}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_strict_missing_vars(self):
        class MySchema(Schema):
            spec = {'bar': IntConfigOption(),
                    'baz': IntConfigOption()}
            foo = DictConfigOption(spec, strict=True)

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]\nbar=2")
        expected_values = {'__main__': {'foo': {'bar': 2, 'baz': 0}}}
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)

    def test_parse_strict_extra_vars(self):
        class MySchema(Schema):
            spec = {'bar': IntConfigOption()}
            foo = DictConfigOption(spec, strict=True)

        config = StringIO("[__main__]\nfoo=mydict\n[mydict]\nbar=2\nbaz=3")
        parser = SchemaConfigParser(MySchema())
        parser.readfp(config)
        self.assertRaises(ValueError, parser.parse_all)


class TestLinesOfDictConfigOption(unittest.TestCase):
    def test_parse_lines_of_dict(self):
        class MySchema(Schema):
            foo = LinesConfigOption(
                        DictConfigOption({'bar': StringConfigOption(),
                                          'baz': IntConfigOption(),
                                          'bla': BoolConfigOption(),
                                          }))
        config = StringIO("""[__main__]
foo = mylist0
      mylist1
[mylist0]
bar=baz
baz=42
bla=Yes
[mylist1]
bar=zort
baz=123
bla=0
""")
        expected_values = {
            '__main__': {'foo': [{'bar': 'baz', 'baz': 42, 'bla': True},
                                {'bar': 'zort', 'baz': 123, 'bla': False},
                               ]}}

        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)


class TestDictWithDicts(unittest.TestCase):
    def test_parse_dict_with_dicts(self):
        innerspec = {'bar': StringConfigOption(),
                     'baz': IntConfigOption(),
                     'bla': BoolConfigOption(),
                    }
        spec = {'name': StringConfigOption(),
                'size': IntConfigOption(),
                'options': DictConfigOption(innerspec)}
        class MySchema(Schema):
            foo = DictConfigOption(spec)
        config = StringIO("""[__main__]
foo = outerdict
[outerdict]
options = innerdict
[innerdict]
bar = something
baz = 42
""")
        expected_values = {
            '__main__': {'foo': {'name': '', 'size': 0,
                                'options': {'bar': 'something', 'baz': 42,
                                            'bla': False}}}}
        schema = MySchema()
        parser = SchemaConfigParser(schema)
        parser.readfp(config)
        self.assertEqual(parser.values(), expected_values)


class TestListOfTuples(unittest.TestCase):
    def setUp(self):
        class MySchema(Schema):
            foo = LinesConfigOption(item=TupleConfigOption(length=3))
        schema = MySchema()
        self.parser = SchemaConfigParser(schema)

    def test_parse_list_of_tuples(self):
        config = StringIO('[__main__]\nfoo = a, b, c\n      d, e, f')
        expected_values = {
            '__main__': {'foo': [('a', 'b', 'c'), ('d', 'e', 'f')]}}
        self.parser.readfp(config)
        self.assertEqual(self.parser.values(), expected_values)

    def test_parse_wrong_tuple_size(self):
        config = StringIO('[__main__]\nfoo = a, b, c\n      d, e')
        self.parser.readfp(config)
        self.assertRaises(ValueError, self.parser.values)

    def test_parse_empty_tuple(self):
        config = StringIO('[__main__]\nfoo=()')
        expected_values = {'__main__': {'foo': [()]}}
        self.parser.readfp(config)
        self.assertEqual(self.parser.values(), expected_values)


if __name__ == '__main__':
    unittest.main()
