from selenium import webdriver

from src.logs.mixin import LogMixin
from src.pages.metal.base import BaseMetalPage


class MetalAluminumPage(BaseMetalPage, LogMixin):
    """Metal aluminum page class."""

    @property
    def metal_url(self) -> str:
        """Return the URL of the page."""
        return "https://www-old.metal.com/price/Base-Metals/Aluminum"

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
