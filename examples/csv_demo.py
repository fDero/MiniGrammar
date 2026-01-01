import sys
from minigrammar import *

class CSVSettings(LanguageSettings):
    @classmethod
    def ignore_characters(cls, char):
        return char == ' ' or char == '\t' or char == '\r'


@repeating("Record", None, None, '\n', False, False)
class Document(CSVSettings):
    def __repr__(self):
        return self.elems.__repr__()


@repeating("Field", None, None, ',', False, False)
class Record(CSVSettings):
    def __repr__(self):
        return self.elems.__repr__()


@regex_pattern(r'^[a-zA-Z0-9_]+$')
class Field(CSVSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        iterator = FileParserIterator(file)
        document = Document(iterator)
        print(document)