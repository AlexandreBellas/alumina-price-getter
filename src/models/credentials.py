from dataclasses import dataclass


@dataclass
class GoogleSheetsCredentials:
    """Google Sheets credentials class."""

    endpoint: str
    token: str
