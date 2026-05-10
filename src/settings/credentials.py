import json
from pathlib import Path

from src.models.credentials import EmailCredentials
from src.validators.credentials import CredentialsValidator


class Credentials:
    """Credentials class."""

    validator: CredentialsValidator

    def __init__(self) -> None:
        # Initialize the validator
        self.validator = CredentialsValidator()

        # Load credentials from file
        with Path.open("credentials.json") as f:
            credentials = json.load(f)

            # Validate file is a dictionary
            if not isinstance(credentials, dict):
                message = "Credentials must be a dictionary"
                raise TypeError(message)

            # Validate "email" presence
            if "email" not in credentials:
                message = "Credentials must contain 'email'"
                raise ValueError(message)

            # Create email credentials
            self.email = self.validator.validate(EmailCredentials, credentials["email"])
