import json

from src.client.driver import DriverBuilder
from src.pages.lme import LmePage
from src.pages.metal.al import MetalAluminumPage
from src.pages.metal.ti import MetalTitaniumPage

# Initialize the driver
driver = DriverBuilder().driver

try:
    prices: dict[str, str] = {}

    # Open the LME page
    lme_page = LmePage(driver)
    lme_page.open()

    # Get the price of the alumina
    prices["lme"] = lme_page.get_price()

    # Open the Metal Aluminum page
    metal_al_page = MetalAluminumPage(driver)
    metal_al_page.open()

    # Get the price of all Aluminum-related products
    bauxite_prices = metal_al_page.get_price("Bauxite")
    alumina_prices = metal_al_page.get_price("Alumina")
    aluminum_hydroxide_prices = metal_al_page.get_price("AluminumHydroxide")
    prices = {**prices, **bauxite_prices, **alumina_prices, **aluminum_hydroxide_prices}

    # Open the Metal Titanium page
    metal_ti_page = MetalTitaniumPage(driver)
    metal_ti_page.open()

    # Get the price of all Titanium-related products
    titanium_dioxide_prices = metal_ti_page.get_price("TitaniumDioxide")
    prices = {**prices, **titanium_dioxide_prices}

    print(f"💰 Prices: {json.dumps(prices, indent=4)}")
except Exception as e:
    print(f"❌ Error: {e}, {e.__traceback__}")
