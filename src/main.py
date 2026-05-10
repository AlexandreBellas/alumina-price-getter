from src.client.driver import DriverBuilder
from src.pages.lme import LmePage

# Initialize the driver
driver = DriverBuilder().driver

try:
    # Open the LME page
    lme_page = LmePage(driver)
    lme_page.open()

    # Get the price of the alumina
    price = lme_page.get_price()
    print(f"💰 Price: {price}")
except Exception as e:
    print(f"❌ Error: {e}, {e.__traceback__}")
