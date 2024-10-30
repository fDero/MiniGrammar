
class ParserStringIterator:
    def __init__(self, source_text):
        self._index = 0
        self._current_line = source_text
        self._generator = None

    def clone(self):
        cloned = ParserStringIterator(self._current_line)
        cloned._index = self._index
        cloned._generator = self
        return cloned

    def advance(self):
        self._index += 1

    def advance_by(self, n):
        self._index += n

    def peek(self):
        if self._index < len(self._current_line):
            return self._current_line[self._index]
        return None

    def get_index(self):
        return self._index

    def synchronize_with_source(self):
        if self._current_line is not None:
            self._generator._current_line = self._current_line
            self._generator._index = self._index