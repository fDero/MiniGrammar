from collections.abc import Callable

class ParserIterator:
    """
    It's used as the one and only parameter for constructors (__init__) of AST-classes where parsing a file is needed.
    This class can be used as a python-iterator (e.g. using next on it) to iterate over characters of an indexable
    source of characters representing the text to be parsed
    """

    def __init__(self, get_at_index: Callable[[int], str]):
        self._index = 0
        self._char_pos = 1
        self._line_number = 1
        self._get_at_index = get_at_index
        self._generator = None

    def __iter__(self):
        return self

    def __next__(self):
        current_value = self.peek()
        if current_value is None:
            raise StopIteration
        self.advance()
        return current_value

    def clone(self) -> 'ParserIterator':
        """
        :return: an independent clone of this iterator, with its own state
        """
        cloned = ParserIterator(self._get_at_index)
        cloned._char_pos = self._char_pos
        cloned._line_number = self._line_number
        cloned._index = self._index
        cloned._generator = self
        return cloned

    def advance(self) -> None:
        """
        Advances the iterator by one character. It doesn't return any value,
        to query for the current value of the iterator use the peek() method
        """
        self._index += 1
        self._char_pos += 1
        if self._get_at_index(self._index) == "\n":
            self._char_pos = 1
            self._line_number += 1

    def advance_by(self, n: int) -> None:
        """
        Advances the iterator by n character. It doesn't return any value,
        to query for the current value of the iterator use the peek() method
        :param n: how many times to advance the iterator
        """
        for _ in range(n):
            self.advance()

    def peek(self) -> str | None:
        """
        Used to see the current value of the iterator without advancing it.
        :return: a string of length 1 corresponding to the current value of the iterator or None if end-of-file is reached.
        """
        current_char = self._get_at_index(self._index)
        if current_char == "":
            return None
        return current_char

    def synchronize_with_source(self) -> None:
        """
        When called on an iterator that has been created using the clone method on another iterator,
        it will update the state of the original iterator to match the state of this iterator. If the
        iterator has not been created as a clone, it does nothing.
        """
        if self._generator is not None:
            self._generator._index = self._index
            self._generator._char_pos = self._char_pos
            self._generator._line_number = self._line_number
