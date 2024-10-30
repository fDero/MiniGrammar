import unittest

from minigrammar.iterators import ParserStringIterator
from minigrammar.parsing import *
from minigrammar.exceptions import *
from minigrammar.language_settings import *


class ParsingRegexPatterns(unittest.TestCase):

    def test_case_digest_everything_successfully(self):
        @regex_pattern(r'\b-?\d+\b')
        class Integer(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10")
        Integer(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_regex_mismatch_left_the_iterator_untouched(self):
        @regex_pattern(r'\b-?\d+\b')
        class Integer(BasicLanguageSettings): pass

        iterator = ParserStringIterator("XX")
        with self.assertRaises(CannotParseException):
            Integer(iterator)
        self.assertTrue("X" == iterator.peek())

    def test_case_regex_mismatch_on_empty_string_left_the_iterator_untouched(self):
        @regex_pattern(r'\b-?\d+\b')
        class Integer(BasicLanguageSettings): pass

        iterator = ParserStringIterator("")
        with self.assertRaises(CannotParseException):
            Integer(iterator)
        self.assertTrue(None == iterator.peek())

    def test_case_regex_ok_on_empty_string_left_the_iterator_untouched(self):
        @regex_pattern(r'')
        class Empty(BasicLanguageSettings): pass

        iterator = ParserStringIterator("")
        Empty(iterator)
        self.assertTrue(None == iterator.peek())


if __name__ == '__main__':
    unittest.main()
