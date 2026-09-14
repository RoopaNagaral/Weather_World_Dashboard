#Pandas cleaning: clean and transform the raw weather data

import pandas as pd

weather_df = pd.read_csv("raw_weather.csv")

print("Raw Data: ")
print(weather_df.head())

print("\nWeather DataFrame Informatno:")
weather_df.info()

print("\nMissing values before cleaning:")
print(weather_df.isna().sum())

print("\nDuplicate rows before cleaning:")
print(weather_df.duplicated().sum())

#standardize the column names
weather_df.rename(
    columns={
        "City": "city",
        "Condition": "condition",
        "Local-Time": "local_time",
        "Source-URL": "source_url",
        "Temperature": "temperature",
        "Scraped-At": "scraped_at",
    },
    inplace=True,
)

#remove extra space from text columns
text_columns = [
    "city",
    "condition",
    "local_time",
    "source_url",
    "temperature"
]

for column in text_columns:
    weather_df[column] = weather_df[column].str.strip()
    
#Convert empty strings into missing values
weather_df.replace("", pd.NA, inplace=True)

#Handle missing city and condition values
weather_df["city"] = weather_df["city"].fillna("unknown")
weather_df["condition"] = weather_df["condition"].fillna("unknown")

#remove duplicate weather records
weather_df.drop_duplicates(inplace=True)

#exctract the numeric temperature
weather_df["temperature_f"] = pd.to_numeric(weather_df["temperature"].str.extract(r"(-?\d+)")[0], errors="coerce")

# Convert Fahrenheit to Celsius
weather_df["temperature_c"] = ((weather_df["temperature_f"] - 32) * 5 / 9).round(1)

# Extract the country from each source url
weather_df["country"] = weather_df["source_url"].str.extract(r"/weather/([^/]+)/")[0]

weather_df["country"] = weather_df["country"].fillna("unknown")

# Convert scraped at to datatime data type
weather_df["scraped_at"] = pd.to_datetime(weather_df["scraped_at"], errors="coerce", utc=True)

# remove original temperature column
weather_df.drop(columns=["temperature"], inplace=True)

print("Clean Data: ")
print(weather_df.head())

print("\nCleaned DataFrame Informatno:")
weather_df.info()

print("\nMissing values after cleaning:")
print(weather_df.isna().sum())

print("\nDuplicate rows after cleaning:")
print(weather_df.duplicated().sum())

# Groupby country
country_weather_summary = (
    weather_df.groupby("country", as_index=False)
    .agg(
        city_count=("city", "count"),
        average_temperature_c=("temperature_c", "mean"),
        minimum_temperature_c=("temperature_c", "min"),
        maximum_temperature_c=("temperature_c", "max")
    )
)


country_weather_summary = country_weather_summary.sort_values("average_temperature_c", ascending=False)

print("\nCountry weather summary:")
print(country_weather_summary.head(10))

# Filter for cities at or below 10 degrees Celsius
colder_cities = weather_df[ weather_df["temperature_c"] <= 10].copy()

colder_cities = colder_cities.sort_values("temperature_c")

print("\nCities at or below 10 degrees celsius:")
print(colder_cities[["city","country","condition","temperature_c"]])

country_weather_summary.to_csv(
    "country_temperature_summary.csv",
    index=False
)

colder_cities.to_csv(
    "colder_cities.csv",
    index=False
)
weather_df.to_csv(
    "clean_weather.csv",
    index=False
)

print("\nCleaned weather data saved to clean_weather.csv")