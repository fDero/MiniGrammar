import unittest

from minigrammar.iterators import ParserStringIterator
from minigrammar.parsing import *
from minigrammar.language_settings import *
from minigrammar.exceptions import *


class ParsingExactMatches(unittest.TestCase):

    def test_case_digest_everything_successfully(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10")
        Number10(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_nothing_to_digest_exception(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        with self.assertRaises(CannotParseException):
            Number10(ParserStringIterator(""))

    def test_case_nothing_to_digest_but_ok(self):
        @exact_match("")
        class Empty(BasicLanguageSettings): pass

        iterator = ParserStringIterator("")
        Empty(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_mismatch_left_the_iterator_untouched(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        iterator = ParserStringIterator("50")
        with self.assertRaises(CannotParseException):
            Number10(iterator)
        self.assertEqual("5", iterator.peek())


if __name__ == '__main__':
    unittest.main()
