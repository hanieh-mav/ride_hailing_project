from typing import Any


class Validation:

    @staticmethod
    def validate_is_integer_type(value: int):
        if not isinstance(value, int):
            raise ValueError('invalid argument type')

    @staticmethod
    def validate_is_float_or_integer_type(value: float):
        if not isinstance(value, float) and not isinstance(value, int):
            raise ValueError('invalid argument type')

    @staticmethod
    def validate_is_float_type(value: float):
        if not isinstance(value, float):
            raise ValueError('invalid argument type')

    @staticmethod
    def validate_variable_existence(variable: Any) -> None:
        if variable is None:
            raise ValueError('invalid argument type')

    @staticmethod
    def validate_is_string_type(variable: str):
        if not isinstance(variable, str):
            raise ValueError('invalid argument type')

    @classmethod
    def validate_is_not_negative_integer_type(cls, variable: Any) -> None:
        cls.validate_is_integer_type(variable)
        if variable < 0:
            raise ValueError('invalid argument type')

    @classmethod
    def validate_is_not_non_negative_float_or_integer_type(cls, variable: Any) -> None:
        cls.validate_is_float_or_integer_type(variable)
        if variable < 0:
            raise ValueError('invalid argument type')
