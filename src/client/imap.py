from email.header import decode_header
from imaplib import IMAP4, IMAP4_SSL

from src.logs.mixin import LogMixin
from src.models.credentials import EmailCredentials


class ImapClient(LogMixin):
    """Builds the IMAP client for the script."""

    def __init__(self, credentials: EmailCredentials):

        super().__init__()

        # Initialize the IMAP client with TLS/SSL
        if credentials.port in {587, 143}:
            client = IMAP4(credentials.server, credentials.port)
            client.starttls()

        # Use SSL/TLS for default IMAP port 993
        else:
            client = IMAP4_SSL(credentials.server, credentials.port or 993)

        # Authenticate
        client.login(credentials.login, credentials.password)

        # Select the inbox
        client.select("INBOX")

        # Store the credentials for convenience
        self.credentials = credentials

        # Save the client
        self.client = client

    def _decode_header(self, header_value: str | None) -> str:
        """Decode email header value."""
        if header_value is None:
            return ""

        decoded_parts = decode_header(header_value)
        decoded_string = ""

        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    decoded_string += part.decode(encoding)
                else:
                    decoded_string += part.decode("utf-8", errors="ignore")
            else:
                decoded_string += str(part)

        return decoded_string

    def close(self) -> None:
        """Close the IMAP connection."""
        self.client.close()
        self.client.logout()
