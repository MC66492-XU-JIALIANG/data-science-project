# Comparative GDP Per Capita and Population Trends

## Research question
How did GDP per capita and total population change in China, Japan, the United Kingdom, and the United States between 2000 and 2024?

## Dataset source and permissions
The project uses the World Bank Indicators API to retrieve two World Development Indicators: GDP per capita (current US$, `NY.GDP.PCAP.CD`) and Population, total (`SP.POP.TOTL`). The World Bank describes the API as programmatic access to its indicator data and states that API keys are not required. Review the World Bank terms of use before redistributing data.

Sources:
- World Bank. (2026). *Indicators API documentation*. https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation
- World Bank. (2026). *World Development Indicators*. https://data.worldbank.org/

## Methods and tools
`analysis.py` retrieves the two indicators for the four selected economies. The repository includes a CSV data snapshot and two line charts: one for GDP per capita and one for population. The visuals were created with Python and Pillow.

## Key findings
The United States remains the highest GDP-per-capita series in this comparison. China rises substantially from a lower starting point. Population trends differ: China slows after its earlier growth, Japan declines in recent years, and the United States continues to rise.

## Limitation
GDP per capita in current US dollars is not adjusted for inflation or purchasing-power differences. This is a descriptive comparison and does not establish causation.

## Run instructions
1. Install Python 3.10 or later.
2. Run `python analysis.py` to download an updated CSV snapshot from the World Bank API.
3. The script recreates the CSV snapshot and both figures in `figures/`. `requirements.txt` records the image-library dependency.

## Project status
Completed for CISC7204 Practice 09. A future revision will add inflation-adjusted series and interactive country selection.
