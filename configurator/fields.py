"""Settings fields"""

from abc import ABC
from typing import Any
import re


class ValidationError(Exception):
    """
    Thrown when value for the Field didn't pass the validation.
    """


class Field(ABC):
    """
    Base Field type. All objects used as settings fields should be subclass of Field.
    """
    type_: type = object
    default: Any = None

    def __init__(self, required: bool = True, default: Any = None):
        """
        Creates new Field object.
        Args:
            required: set true if field is crucial for the project and should be always provided
            default: default field value if not specified in config
        """
        self.required = required
        if default is not None:
            self.default = self.validate(default)

    def validate(self, value: Any) -> Any:
        """
        Validate if value can be assign to the field.
        Checks if value's type is correct.
        Args:
            value: value to assign to the Field

        Returns:
            safe to assign value

        """
        if not isinstance(value, self.type_):
            raise ValidationError('Type mismatch')
        return value


class Integer(Field):
    """
    Class for number type fields.
    """
    type_ = int
    default = 0


class PositiveInteger(Integer):
    """
    Class for positive integers - natural numbers.
    """
    default = 1

    def validate(self, value: int) -> int:
        value = super().validate(value)
        if value <= 0:
            raise ValidationError('PositiveInteger value must be greater than 0.')
        return value


class String(Field):
    """
    Class for string type fields.
    """
    type_ = str
    default = ''


class Email(String):
    """
    Class for email fields.
    """

    def validate(self, value: str) -> str:
        """Validates email using simple regex."""
        value = super().validate(value)
        regex = re.compile(r'^\S+@\S+\.\S+$')
        if regex.fullmatch(value) is None:
            raise ValidationError('Provided string is not a valid email.')
        return value


class Boolean(Field):
    """
    Class for bool type fields.
    """
    type_ = bool
    default = False


class Float(Field):
    """
    Class for floating-point numbers.
    """
    type_ = float
    default = 0.0


class Url(String):
    """
    Class for url fields.
    """

    def validate(self, value: str) -> str:
        """Validates url using regular expression."""
        value = super().validate(value)
        regex = regex = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if regex.fullmatch(value) is None:
            raise ValidationError('Provided string is not a valid url.')
        return value
