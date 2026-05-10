from selenium import webdriver
from selenium_stealth import stealth

from src.settings.config import config


class DriverBuilder:
    """Builds the web driver for the script.

    @see https://www.zenrows.com/blog/selenium-avoid-bot-detection#remove-javascript-signature
    @see https://stackoverflow.com/questions/75678008/login-redirects-to-unavilable-when-i-use-selenium
    """

    def __init__(self, *, disable_web_security: bool = False):

        # Initialize the driver options with arguments that hides the bot presence
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-agent={config.user_agent}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--no-sandbox")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", value=False)
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--start-maximized")

        if disable_web_security:
            options.add_argument("--disable-web-security")

        caps = webdriver.DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        # Initialize the driver
        driver = webdriver.Chrome(options=options)

        # Execute script to hide the bot presence
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        # Save the driver
        self.driver = driver
