class BasicLanguageSettings:
    context = {}

    @classmethod
    def get_id(cls):
        return f"{cls.__module__}.{cls.__qualname__}"

    @classmethod
    def ignore_characters(cls, char):
        return char == ' ' or char == '\t' or char == '\n' or char == '\r'