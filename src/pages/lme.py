from selenium import webdriver
from selenium.webdriver.common.by import By

from src.pages.base import BasePage


class LmePage(BasePage):
    """LME page."""

    url = "https://www.lme.com/metals/non-ferrous/lme-alumina_"

    def __init__(self, driver: webdriver.Chrome) -> None:
        super().__init__(driver=driver, url=self.url)

    def get_price(self) -> str:
        """Get the price of the alumina."""
        return self.find_element(By.CSS_SELECTOR, "span.hero-metal-data__number").text
