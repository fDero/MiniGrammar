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

        @either({Hello.get_id(), Number10.get_id()})
        class Number10OrHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("Hello")
        Number10OrHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_digest_everything_successfully2(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @either({Hello.get_id(), Number10.get_id()})
        class Number10OrHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10")
        Number10OrHello(iterator)
        self.assertEqual(None, iterator.peek())

    def test_case_no_case_matches(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @exact_match("Hello")
        class Hello(BasicLanguageSettings): pass

        @either({Hello.get_id(), Number10.get_id()})
        class Number10OrHello(BasicLanguageSettings): pass

        iterator = ParserStringIterator("XX")
        with self.assertRaises(CannotParseException):
            Number10OrHello(iterator)
        self.assertEqual("X", iterator.peek())


if __name__ == '__main__':
    unittest.main()
