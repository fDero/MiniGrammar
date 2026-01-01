from collections.abc import Callable
from typing import TextIO


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
        self._snapshots = []

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
        cloned._snapshots = self._snapshots
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

    def snapshot(self, offset : int = 0):
        """
        Used to save the current coordinates of the iterator and later recover the location of an error 
        even in cases where the original iterator has been advanced or restored to a previous state.
        """
        self._snapshots.append((self._line_number, self._char_pos - offset))

    def inspect_for_errors(self) -> tuple[int, int]:
        """
        Used to get the furthest snapshot saved so far, which corresponds to the location of the most 
        advanced error. This always returns something even if no exception were raised during parsing.
        You should only care about inspecting for errors if you catched an exception in a try/catch block.
        :return: a tuple (line_number, char_pos) corresponding to the furthest snapshot saved so far.
        """
        if len(self._snapshots) == 0:
            return (1, 1)
        return max(self._snapshots, key=lambda x: (x[0], x[1]))



class FileParserIterator(ParserIterator):
    """
    It's used as the one and only parameter for constructors (__init__) of AST-classes where parsing
    a file is needed. This class can be used as a python-iterator (e.g. using next on it) to iterate
    over characters of a file. It must be constructed from a file already opened in read mode,
    corresponding to the file to parse.
    """

    def __init__(self, source_file: TextIO):
        def get_at_index(index: int):
            source_file.seek(index)
            current_char = source_file.read(1)
            source_file.seek(index)
            return current_char

        super().__init__(get_at_index)


class StringParserIterator(ParserIterator):
    """
    It's used as the one and only parameter for constructors (__init__) of AST-classes where parsing a
    file is needed. This class can be used as a python-iterator (e.g. using next on it) to iterate
    over characters of a string. It must be constructed from a string containing text to parse.
    """

    def __init__(self, source_text: str):
        def get_at_index(index: int):
            if index >= len(source_text):
                return None
            else:
                return source_text[index]

        super().__init__(get_at_index)