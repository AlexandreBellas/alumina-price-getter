from abc import ABC
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select, WebDriverWait

from src.logs.mixin import LogMixin


class BasePage(LogMixin, ABC):
    """Base class for all pages."""

    def __init__(self, driver: webdriver.Chrome, url: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.driver = driver
        self.url = url

    def open(self, *, timeout: int = 5, save_html: bool = True) -> bool:
        """Open the page `url` with a timeout of `timeout` seconds."""
        self.debug(f"🔁 Opening page {self.url}...")

        try:
            # Open the page
            self.driver.get(self.url)

            # Wait for the page to be loaded
            WebDriverWait(self.driver, timeout).until(ec.url_contains(self.url))
            self.debug(f"✅ Page {self.url} opened successfully.")

            if save_html:
                if not Path.exists("snapshots"):
                    Path.mkdir("snapshots", parents=True)

                with Path.open(
                    f"snapshots/{self.__class__.__name__}-{datetime.now(timezone(timedelta(hours=-3))).strftime('%Y-%m-%d-%H-%M-%S')}.html",
                    "w",
                ) as f:
                    f.write(self.driver.page_source)

            return True
        except TimeoutException:
            self.error(f"❌ Failed to open page {self.url} after {timeout} seconds")
            return False
        except Exception as e:
            self.error(f"❌ Failed to open page {self.url}: {e}")
            return False

    def check_open(self, *, timeout: int = 5, tolerance: int = 100) -> bool:
        """Check if the page is open `tolerance` times with a timeout of `timeout` seconds."""
        self.debug(f"🔁 Checking if page {self.url} is open (timeout: {timeout}, tolerance: {tolerance})...")

        i = 0
        while i < tolerance:
            try:
                self.debug(
                    f'🔁 Attempt {i} to check if page "{self.url}" is open (timeout: {timeout}, tolerance: {tolerance})'
                )
                if self.url in self.driver.current_url:
                    self.debug(f'✅ Page "{self.url}" is open.')
                    return True
                self.debug(f'🔁 Page "{self.url}" is not yet opened (current URL: "{self.driver.current_url}").')
            except Exception:
                self.debug(f'🔁 Page "{self.url}" is not yet opened (current URL: "{self.driver.current_url}").')

            sleep(timeout)
            i += 1

        self.error(
            f'❌ Failed to check if page "{self.url}" is open after "{tolerance}" attempts with timeout "{timeout}"'
        )
        return False

    def try_open(self, *, timeout: int = 5, tolerance: int = 100) -> bool:
        """Try to open the page `tolerance` times with a timeout of `timeout` seconds."""
        self.debug(f"🔁 Trying to open page {self.url} (timeout: {timeout}, tolerance: {tolerance})...")

        i = 0
        while i < tolerance:
            self.debug(f"🔁 Attempt {i} to open page {self.url} (timeout: {timeout}, tolerance: {tolerance})")
            is_successful = self.open(timeout=timeout)
            i += 1

            if is_successful:
                self.debug(f"✅ Page {self.url} opened successfully.")
                return True

        self.error(f'❌ Failed to open page {self.url} after "{tolerance}" attempts with timeout "{timeout}"')
        return False

    def find_element(self, by: By, value: str) -> WebElement:
        """Find the element identified by `by` and `value`."""
        # Find the element and return it
        return self.driver.find_element(by, value)

    def find_elements(self, by: By, value: str) -> list[WebElement]:
        """Find the elements identified by `by` and `value`."""
        # Find the elements and return them
        return self.driver.find_elements(by, value)

    def write(self, by: By, value: str, text: str) -> None:
        """Write `text` into the element identified by `by` and `value`."""
        # Build an action chains for mouse movements and clicks
        action = ActionChains(self.driver)

        # Move the mouse over the element and click it
        action.move_to_element(self.find_element(by, value)).perform()
        action.click().perform()

        # Send the text to the element
        action.send_keys(text).perform()

    def click(self, *, element: WebElement | None = None, by: By = By.ID, value: str = "") -> None:
        """Click the element identified by `by` and `value` or the given `element`."""
        # Build an action chains for mouse movements and clicks
        action = ActionChains(self.driver)

        # Move the mouse over the element and click it
        action.move_to_element(element or self.find_element(by, value)).perform()
        action.click().perform()

    def select(self, by: By, value: str, text: str) -> None:
        """Select the option identified by `by` and `value`."""
        # Build an action chains for mouse movements and clicks
        action = ActionChains(self.driver)

        # Find the select element
        select_element = self.find_element(by, value)

        # Move the mouse over the element and click it
        action.move_to_element(select_element).perform()
        action.click().perform()

        # Initialize the select element and select the option by visible text
        select = Select(select_element)
        select.select_by_visible_text(text)

    def attach(self, by: By, value: str, file_path: str) -> None:
        """Attach a file to the element identified by `by` and `value`."""
        # Build an action chain for only mouse movements
        action = ActionChains(self.driver)

        # Find the file input element
        file_input = self.find_element(by, value)

        # Move the mouse over the element
        action.move_to_element(file_input).perform()

        # Make the file input element receive the file path
        file_input.send_keys(file_path)

    def wait_for_input(
        self,
        by: By,
        value: str,
        validator: Callable[[str], bool] | None,
        *,
        timeout: int = 5,
        tolerance: int = 100,
        identifier: str | None = None,
    ) -> bool:
        """Wait for an input element identified by `by` and `value` to have a content, optionally using `validator`."""
        element = self.find_element(by, value)
        input_identifier = f'"{identifier}" input' if identifier else "input"

        i = 0
        while i < tolerance:
            self.debug(f"🔁 Attempt {i} to wait for {input_identifier} (timeout: {timeout}, tolerance: {tolerance})")

            content = element.get_attribute("value")
            if content and (not validator or validator(content)):
                self.debug(f"✅ {input_identifier} found: {content}")
                return True

            sleep(timeout)
            i += 1

        self.error(f'❌ Failed to wait for {input_identifier} after "{tolerance}" attempts with timeout "{timeout}"')
        return False

    def alert(self, message: str) -> None:
        """Alert the user with a message."""
        self.driver.execute_script(f"alert('{message}')")

    def exists(self, by: By, value: str) -> bool:
        """Check if the element identified by `by` and `value` exists."""
        try:
            self.find_element(by, value)
        except NoSuchElementException:
            return False
        else:
            return True
