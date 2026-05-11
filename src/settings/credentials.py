import json
from json.decoder import JSONDecodeError
from pathlib import Path

from src.models.credentials import GoogleSheetsCredentials
from src.validators.credentials import CredentialsValidator


class Credentials:
    """Credentials class."""

    validator: CredentialsValidator

    def __init__(self) -> None:
        # Initialize the validator
        self.validator = CredentialsValidator()

        # Load credentials from file
        with Path.open("credentials.json") as f:
            try:
                credentials = json.load(f)

                # Validate file is a dictionary
                if not isinstance(credentials, dict):
                    message = "Credentials must be a dictionary"
                    raise TypeError(message)

                # Validate "google_sheets" presence
                if "google_sheets" not in credentials:
                    message = "Credentials must contain 'google_sheets'"
                    raise ValueError(message)

                # Create google sheets credentials
                self.google_sheets = self.validator.validate(GoogleSheetsCredentials, credentials["google_sheets"])
            except JSONDecodeError as e:
                message = "Credentials file (credentials.json) does not have a valid JSON format."
                raise TypeError(message) from e
