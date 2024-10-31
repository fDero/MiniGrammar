import unittest

from minigrammar.iterators import ParserStringIterator
from minigrammar.language_settings import BasicLanguageSettings
from minigrammar.parsing import *
from minigrammar.exceptions import *


class ParsingEither(unittest.TestCase):

    def test_case_digest_everything_successfully(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @chain({Hello.get_id(), Number10.get_id()})
        class Number10ThenHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10Hello")
        Number10ThenHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_full_mismatch(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @chain({Hello.get_id(), Number10.get_id()})
        class Number10ThenHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("XX")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual("X", iterator.peek())

    def test_case_full_mismatch_on_empty_string(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @chain({Hello.get_id(), Number10.get_id()})
        class Number10ThenHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_full_partial_mismatch(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @chain({Hello.get_id(), Number10.get_id()})
        class Number10ThenHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual("1", iterator.peek())

    def test_case_full_partial_mismatch2(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @chain({Hello.get_id(), Number10.get_id()})
        class Number10ThenHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10He")
        with self.assertRaises(CannotParseException):
            Number10ThenHello(iterator)
        self.assertEqual("1", iterator.peek())


if __name__ == '__main__':
    unittest.main()