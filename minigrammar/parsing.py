
from .exceptions import *

import re
import io

def _ignore_every_non_important_character(clazz, iterator_copy):
    while clazz.ignore_characters(iterator_copy.peek()):
        iterator_copy.advance()

def _attempt_parse_exact_match(keyword_or_symbol, iterator_copy, fail_is_error):
    for char in keyword_or_symbol:
        if iterator_copy.peek() != char:
            if fail_is_error:
                raise CannotParseException()
            else:
                return None
        iterator_copy.advance()
    return keyword_or_symbol


def _keep_parsing_until_regex_match(pattern, string_buffer, iterator_copy):
    while iterator_copy.peek() is not None:
        if re.match(pattern, string_buffer.getvalue()):
            break
        string_buffer.write(iterator_copy.peek())
        iterator_copy.advance()


def _keep_parsing_until_regex_fail(pattern, string_buffer, iterator_copy):
    while iterator_copy.peek() is not None:
        if not re.match(pattern, string_buffer.getvalue() + iterator_copy.peek()):
            break
        string_buffer.write(iterator_copy.peek())
        iterator_copy.advance()


def _pretend_ignored_trailing_character_or_none(ignore_characters_callback, iterator_copy):
    if (iterator_copy.peek() is not None) and (not ignore_characters_callback(iterator_copy.peek())):
        raise CannotParseException()


def _pretend_regex_match(pattern, string_buffer):
    if not re.match(pattern, string_buffer.getvalue()):
        raise CannotParseException()


def _attempt_parse_rule_by_name(context, rule_name, iterator_copy, fail_is_error):
    try:
        return context[rule_name](iterator_copy)
    except CannotParseException:
        if fail_is_error:
            raise CannotParseException()
        else:
            return None


def _pretend_counter_within_bounds(counter, minimum, maximum):
    if minimum is not None and counter <= minimum:
        raise CannotParseException()
    if maximum is not None and counter >= maximum:
        raise CannotParseException()


def exact_match(keyword_or_symbol):
    def set_keyword_or_symbol_pattern_on_class(clazz):
        clazz.context[clazz.get_id()] = clazz
        def custom__init__(self, iterator_over_input_token_stream):
            iterator_copy = iterator_over_input_token_stream.clone()
            _ignore_every_non_important_character(clazz, iterator_copy)
            _attempt_parse_exact_match(keyword_or_symbol, iterator_copy, True)
            iterator_copy.synchronize_with_source()
            self.elems = [keyword_or_symbol]
        setattr(clazz, "__init__", custom__init__)
        return clazz
    return set_keyword_or_symbol_pattern_on_class


def regex_pattern(pattern):
    def set_regex_pattern_on_class(clazz):
        clazz.context[clazz.get_id()] = clazz
        def custom__init__(self, iterator_over_input_token_stream):
            iterator_copy = iterator_over_input_token_stream.clone()
            string_buffer = io.StringIO()
            _ignore_every_non_important_character(clazz, iterator_copy)
            _keep_parsing_until_regex_match(pattern, string_buffer, iterator_copy)
            _pretend_regex_match(pattern, string_buffer)
            _keep_parsing_until_regex_fail(pattern, string_buffer, iterator_copy)
            _pretend_ignored_trailing_character_or_none(clazz.ignore_characters, iterator_copy)
            iterator_copy.synchronize_with_source()
            self.elems = [string_buffer.getvalue()]
        setattr(clazz, "__init__", custom__init__)
        return clazz
    return set_regex_pattern_on_class


def repeating(rule_name, minimum, maximum, delimiter, allow_trailing, enforce_trailing):
    def set_multiple_repeating_rules_on_class(clazz):
        clazz.context[clazz.get_id()] = clazz
        def custom__init__(self, iterator_over_input_token_stream):
            iterator_copy = iterator_over_input_token_stream.clone()
            _ignore_every_non_important_character(clazz, iterator_copy)
            parsed_element = _attempt_parse_rule_by_name(clazz.context, rule_name, iterator_copy, minimum is not None and minimum <= 0)
            counter = 0 if parsed_element is None else 1
            extracted_delimiter = delimiter
            self.elems = [parsed_element]
            while parsed_element is not None and extracted_delimiter is not None:
                _ignore_every_non_important_character(clazz, iterator_copy)
                extracted_delimiter = _attempt_parse_exact_match(delimiter, iterator_copy, enforce_trailing)
                if extracted_delimiter is not None:
                    _ignore_every_non_important_character(clazz, iterator_copy)
                    parsed_element = _attempt_parse_rule_by_name(clazz.context, rule_name, iterator_copy, not allow_trailing)
                    self.elems.append(parsed_element)
                counter += 1
            _pretend_counter_within_bounds(counter, minimum, maximum)
            iterator_copy.synchronize_with_source()
        setattr(clazz, "__init__", custom__init__)
        return clazz
    return set_multiple_repeating_rules_on_class


def chain(rule_names):
    def set_multiple_sequential_rules_on_class(clazz):
        clazz.context[clazz.get_id()] = clazz
        def custom__init__(self, iterator_over_input_token_stream):
            iterator_copy = iterator_over_input_token_stream.clone()
            _ignore_every_non_important_character(clazz, iterator_copy)
            self.elems = []
            for r_name in rule_names:
                parsed_element = _attempt_parse_rule_by_name(clazz.context, r_name, iterator_copy, True)
                self.elems.append(parsed_element)
            iterator_copy.synchronize_with_source()
        setattr(clazz, "__init__", custom__init__)
        return clazz
    return set_multiple_sequential_rules_on_class


def either(rule_names):
    def set_mutually_exclusive_rules_on_class(clazz):
        clazz.context[clazz.get_id()] = clazz
        def custom__init__(self, iterator_over_input_token_stream):
            iterator_copy = iterator_over_input_token_stream.clone()
            _ignore_every_non_important_character(clazz, iterator_copy)
            for r_name in rule_names:
                self._elem = _attempt_parse_rule_by_name(clazz.context, r_name, iterator_copy, False)
                if self._elem is not None:
                    self.elems = [self._elem]
                    iterator_copy.synchronize_with_source()
                    return
            raise CannotParseException()
        setattr(clazz, "__init__", custom__init__)
        return clazz
    return set_mutually_exclusive_rules_on_class