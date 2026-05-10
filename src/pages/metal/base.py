from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.common.by import By

from src.logs.mixin import LogMixin
from src.pages.base import BasePage


class BaseMetalPage(BasePage, LogMixin, ABC):
    """Base metal page class."""

    PRICE_ROW_CELL_COUNT = 4
    """Price range, average, change, date"""

    PRICE_ROW_XPATH = ".//div[*[1][self::a]][count(./div) >= 4]"
    """
    Rows: first element child is the product link ``a``; trailing columns are ``div`` siblings
    (price range, average, change, date). No URL or class assumptions.
    """

    @property
    @abstractmethod
    def metal_url(self) -> str:
        """Return the URL of the page."""

    def __init__(self, driver: webdriver.Chrome):
        super().__init__(driver, self.metal_url)

    def get_price(self, section_id: str) -> dict[str, str]:
        """Return each price-table row in the block ``section_id`` as label -> {price, date}.

        ``section_id`` is the DOM ``id`` of the price list block (e.g. the commodity name on
        metal.com). Rows are any ``div`` whose first element child is an ``a`` (label link)
        and which has at least four direct ``div`` children for table cells. ``price`` is the
        average column (second cell).
        """
        section = self.find_element(By.ID, section_id)
        rows: dict[str, str] = {}
        for row in section.find_elements(By.XPATH, self.PRICE_ROW_XPATH):
            link = row.find_element(By.XPATH, "./a[1]")
            spans = link.find_elements(By.XPATH, "./span")
            label = (spans[0].text if spans else link.text).strip()
            if not label:
                continue
            cells = row.find_elements(By.XPATH, "./div")
            if len(cells) < self.PRICE_ROW_CELL_COUNT:
                continue

            price = cells[1].text.strip()
            rows[label] = price

        return rows
