# Weather World Dashboard

A weather exploration project built with Selenium, Pandas, SQLite, Plotly, and Streamlit.

## Deployed Dashboard

[Open the World Weather Dashboard](https://weatherworlddashboard-zzp8x9bnnvawrymfkbs4gh.streamlit.app/)

The dashboard displays saved weather observations. It does not automatically retrieve live weather. The latest scrape timestamp is displayed in the app.

## Data Source and Processing

The scraper collects city names, weather conditions, local times, temperatures, source URLs, and scrape timestamps from https://www.timeanddate.com/weather/.

The cleaning script removes duplicates, handles missing values, converts Fahrenheit temperatures to Celsius, and extracts country labels from source URLs. The database loader stores four datasets in SQLite:

- `raw_weather`
- `clean_weather`
- `country_temperature_summary`
- `hot_cities`

Country labels follow the website's URL categories. Country averages describe the sampled observations rather than national weather averages.

## Dashboard Features

The dashboard reads the `clean_weather` table from `weather_data.db` and displays:

- Average temperature by country
- Temperature distribution
- Observation counts by weather condition

Country, condition, and temperature-range filters update all three charts. Users can switch between Celsius and Fahrenheit, inspect filtered observations, and download them as CSV.

## Run Locally on Windows

Run these commands from the main project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Keep `weather_data.db` beside `streamlit_app.py`. The included database allows the dashboard to run without scraping the website.

## Refresh the Saved Data

The scraper requires Google Chrome. To collect new observations, clean them, and replace the database tables, run these commands in order from the main project folder:

```powershell
.\.venv\Scripts\python.exe .\scrape-weather.py
.\.venv\Scripts\python.exe .\clean-weather.py
.\.venv\Scripts\python.exe .\load-weather-db.py
```

These commands overwrite the saved CSV datasets and database tables. Updating the local database does not update the deployed app until the updated database is committed and pushed to the deployed branch.

## Project Files

- `scrape-weather.py`: retrieves website observations
- `clean-weather.py`: cleans data and creates summaries
- `load-weather-db.py`: imports CSV datasets into SQLite
- `streamlit_app.py`: runs the interactive dashboard
- `weather_data.db`: saved SQLite database
- `raw_weather.csv`: original observations
- `clean_weather.csv`: cleaned observations
- `country_temperature_summary.csv`: country summaries
- `hot_cities.csv`: observations at or above 30°C
- `requirements.txt`: project dependencies
- `service_urls.txt`: deployed dashboard URL

## Deployment

The app is deployed on Streamlit Community Cloud from the `database` branch of `RoopaNagaral/Weather_World_Dashboard`, using `streamlit_app.py` as its entry point.