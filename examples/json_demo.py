import sys
from minigrammar import *


class JsonSettings(LanguageSettings):
    @classmethod
    def ignore_characters(cls, char):
        return char == ' ' or char == '\t' or char == '\r' or char == '\n'


@either(["Array", "Value", "Object"])
class Json(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@chain(["OpenSquareBracket", "MultipleArrayElems", "ClosedSquareBracket"])
class Array(JsonSettings):
    def __repr__(self):
        return "[" + self.elems[1].__repr__() + "]"


@chain(["OpenCurlyBracket", "MultipleObjectFields", "ClosedCurlyBracket"])
class Object(JsonSettings):
    def __repr__(self):
        return "{" + self.elems[1].__repr__() + "}"


@repeating("Json", None, None, ',', False, False)
class MultipleArrayElems(JsonSettings):
    def __repr__(self):
        return self.elems.__repr__()[1:-1]


@repeating("ObjectField", None, None, ',', False, False)
class MultipleObjectFields(JsonSettings):
    def __repr__(self):
        return self.elems.__repr__()[1:-1]


@chain(["StringLiteral", "Colon", "Json"])
class ObjectField(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__() + " : " + self.elems[2].__repr__()


@either(["StringLiteral", "FloatingPointLiteral", "IntegerLiteral", "BooleanLiteral", "NullLiteral"])
class Value(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^"(?:[^"\\]|\\.)*"$')
class StringLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()[1:-1]


@exact_match("null")
class NullLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^\d+$')
class IntegerLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^\d*\.\d+$')
class FloatingPointLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'true|false')
class BooleanLiteral(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("[")
class OpenSquareBracket(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("]")
class ClosedSquareBracket(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("{")
class OpenCurlyBracket(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match("}")
class ClosedCurlyBracket(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match(":")
class Colon(JsonSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as file:
        iterator = FileParserIterator(file)
        json = Json(iterator)
        print(json)