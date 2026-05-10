from dataclasses import dataclass
from typing import Literal


@dataclass
class EmailCredentials:
    """Email credentials class."""

    server: str
    port: int
    protocol: Literal["imap", "pop3"]
    login: str
    password: str
