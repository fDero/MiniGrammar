import unittest

from minigrammar.iterators import ParserStringIterator
from minigrammar.language_settings import BasicLanguageSettings
from minigrammar.parsing import *
from minigrammar.exceptions import *


class ParsingRepeating(unittest.TestCase):

    def test_case_ok_with_trailing_allowed_not_enforced_not_used_well_far_apart(self):
        @exact_match("10")
        class Number10(BasicLanguageSettings): pass

        @repeating(Number10.get_id(), None, None, ',', True, False)
        class Numbers(BasicLanguageSettings): pass

        iterator = ParserStringIterator("10,10,10")
        Numbers(iterator)
        self.assertEqual(None, iterator.peek())


if __name__ == '__main__':
    unittest.main()
