import logging
import sys

from src.settings.config import config


class LogMixin:
    """Mixin for logging."""

    def __init__(self) -> None:
        log_level = logging.DEBUG if config.debug else logging.INFO

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(log_level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)

        self.logger.addHandler(handler)

    def debug(self, message: str) -> None:
        """Debug log."""
        if config.debug:
            self.logger.debug(message)

    def info(self, message: str) -> None:
        """Info log."""
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """Warning log."""
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """Error log."""
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """Critical log."""
        self.logger.critical(message)
