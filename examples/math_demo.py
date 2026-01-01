from minigrammar import *


class MathSettings(LanguageSettings):

    @classmethod
    def ignore_characters(cls, char):
        return char == ' ' or char == '\t' or char == '\r' or char == '\n'


@repeating("Addend", 1, None, '+', False, False)
class Expression(MathSettings):
    def __repr__(self):
        string = self.elems[0].__repr__()
        for elem in self.elems[1:]:
            string += " + " + repr(elem)
        return " { " + string + " } "


@repeating("Factor", 1, None, '*', False, False)
class Addend(MathSettings):
    def __repr__(self):
        string = self.elems[0].__repr__()
        for elem in self.elems[1:]:
            string += " * " + repr(elem)
        return " { " + string + " } "


@either(["Number", "Variable", "WrappedExpression"])
class Factor(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^\d+$')
class Number(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@regex_pattern(r'^[a-z]$')
class Variable(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@chain(["OpenParen", "Expression", "ClosedParen"])
class WrappedExpression(MathSettings):
    def __repr__(self):
        return " ( " + self.elems[1].__repr__() + " ) "


@exact_match("(")
class OpenParen(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


@exact_match(")")
class ClosedParen(MathSettings):
    def __repr__(self):
        return self.elems[0].__repr__()


if __name__ == "__main__":
    iterator = StringParserIterator("x*(a+b)")
    expr = Expression(iterator)
    print(expr)
