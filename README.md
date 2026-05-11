**Disclaimer**: this project has only educational purposes, and does not intend to commercialize, support, or enforce practices that go against the law. The author of this project does not take any responsibility of its usage by readers. Please, use this tool wisely.

# Alumina price getter

A selenium project to obtain Alumina prices automatically and save to a Google Sheets spreadsheet through a Apps Script endpoint.

Gets prices from the following websites:
- [LME Alumina (Platts)](https://www.lme.com/metals/non-ferrous/lme-alumina_)
- [Metal prices - Aluminum](https://www-old.metal.com/price/Base-Metals/Aluminum)
- [Metal prices - Titanium](https://www-old.metal.com/price/Minor-Metals/Titanium)

## How to run

### Step 1. Clone the repository

Open a new terminal and run the following:

```bash
git clone https://github.com/AlexandreBellas/alumina-price-getter
```

You can also download the ZIP file directly from the UI instead.

### Step 2. Install dependencies

In the terminal, navigate to the folder you cloned and execute one of the commands below:

```bash
uv sync --all-groups
```
```bash
# In case you don't have `uv` installed
python -m venv .venv
source .venv/bin/activate
pip install .
```

### Step 3. Configure the credentials

You'll have to create a `credentials.json` file in the project root folder.

The file has the following format:

```json
{
    "google_sheets": {
        "endpoint": "<apps-script-endpoint>",
        "token": "<your-created-token-here>"
    }
}
```

For the endpoint definition, deploy an apps script web project with the code defined in `scripts` folder. Make sure to have a target spreadsheet configured for this web project.

For the token definition, make sure to match its value with the `AUTH_TOKEN` value defined in `scripts/index.gs`.

### Step 4. Run the project

To obtain the alumina prices, run one of the commands below:

```bash
uv run -m src.main
```

```bash
# In case you don't have `uv` installed
python -m src.main
```