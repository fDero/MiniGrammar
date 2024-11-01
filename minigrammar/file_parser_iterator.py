
class FileParserIterator:
    def __init__(self, source_file):
        self._index = 0
        self._source_file = source_file
        self._generator = None

    def __iter__(self):
        return self

    def __next__(self):
        current_value = self.peek()
        if current_value is None:
            raise StopIteration
        self.advance()
        return current_value

    def clone(self):
        cloned = FileParserIterator(self._source_file)
        cloned._index = self._index
        cloned._generator = self
        return cloned

    def advance(self):
        self._index += 1

    def advance_by(self, n):
        self._index += n

    def peek(self):
        self._source_file.seek(self._index)
        current_char = self._source_file.read(1)
        self._source_file.seek(self._index)
        if current_char == "":
            return None
        return current_char

    def get_index(self):
        return self._index

    def synchronize_with_source(self):
        if self._source_file is not None:
            self._generator._index = self._index