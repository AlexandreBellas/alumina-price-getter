from selenium import webdriver

from src.pages.metal.base import BaseMetalPage


class MetalTitaniumPage(BaseMetalPage):
    """Metal titanium page class."""

    @property
    def metal_url(self) -> str:
        """Return the URL of the page."""
        return "https://www-old.metal.com/price/Minor-Metals/Titanium"

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver)
