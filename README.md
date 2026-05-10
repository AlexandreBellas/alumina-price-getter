**Disclaimer**: this project has only educational purposes, and does not intend to commercialize, support, or enforce practices that go against the law. The author of this project does not take any responsibility of its usage by readers. Please, use this tool wisely.

# Alumina price getter

A selenium project to obtain Alumina prices automatically.

Gets the Alumina price from the following websites:
- [LME Alumina (Platts)](https://www.lme.com/metals/non-ferrous/lme-alumina_)

## Installing dependencies

Execute the command below (make sure to have `uv` installed):

```bash
uv sync --all-groups
```

## Running the project

To obtain the alumina prices, run:

```bash
uv run python -m src.main
```