class CannotParseException(Exception):
    def __init__(self, iterator):
        line_number, char_position = iterator.inspect_for_errors()
        super().__init__(f"Can't parse the given entity at line {line_number}, character {char_position}")
