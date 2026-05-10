from dataclasses import is_dataclass
from typing import Any, Literal, TypeVar, get_args, get_origin

T = TypeVar("T")


class CredentialsValidator:
    """Credentials validator class."""

    def validate(self, dataclass: type[T], credentials: Any) -> T:
        """Validate if the credentials given are valid for the given dataclass."""
        # Validate `dataclass` is a dataclass
        if not is_dataclass(dataclass):
            message = "'dataclass' must be a dataclass"
            raise TypeError(message)

        # Validate `credentials` is a dict
        if not isinstance(credentials, dict):
            message = "'credentials' must be a dictionary"
            raise TypeError(message)

        # Validate credentials contains all fields of the dataclass
        if not all(key in credentials for key in dataclass.__dataclass_fields__):
            raise ValueError(
                "'credentials' must contain these fields: " + ", ".join(dataclass.__dataclass_fields__.keys())
            )

        # Validate each field of the dataclass
        for key, value in dataclass.__dataclass_fields__.items():
            # Validate literals
            if get_origin(value.type) is Literal:
                if credentials[key] not in (args := get_args(value.type)):
                    message = f"'{key}' must be one of {args}"
                    raise ValueError(message)

                continue

            # Validate other types
            if not isinstance(credentials[key], value.type):
                message = f"'{key}' must be a {value.type}"
                raise TypeError(message)

        # Validate values are not empty
        for key in dataclass.__dataclass_fields__:
            if isinstance(credentials[key], str) and not credentials[key]:
                message = f"'{key}' must not be empty"
                raise ValueError(message)

        # Return instantiated dataclass
        return dataclass(**credentials)
