from typing import TextIO

from minigrammar import ParserIterator


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
