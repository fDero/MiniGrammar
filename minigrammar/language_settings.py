class BasicLanguageSettings:
    context = {}

    def __init__(self):
        self.elems = []

    @classmethod
    def get_id(cls):
        return f"{cls.__module__}.{cls.__qualname__}"

    @classmethod
    def get_id_of_rule_assuming_in_same_module(cls, class_name):
        id_of_settings_class_without_last_part = cls.get_id()
        while id_of_settings_class_without_last_part[-1] != '.':
            id_of_settings_class_without_last_part = id_of_settings_class_without_last_part[:-1]
        return id_of_settings_class_without_last_part + class_name

    @classmethod
    def ignore_characters(cls, char):
        return char == ' ' or char == '\t' or char == '\n' or char == '\r'