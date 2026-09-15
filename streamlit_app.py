from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st  # Importing the Streamlit library

# -----------------------------
# Load data from SQLite
# -----------------------------
database_path = Path(__file__).resolve().parent / "weather_data.db"
if not database_path.is_file():
    st.error("Place weather_data.db inside streamlit.py before running the file")
    st.stop()
    
try:
    with sqlite3.connect(database_path.as_uri()+ "?mode=ro", uri=True) as conn:
        df = pd.read_sql_query("SELECT * FROM clean_weather", conn)
except (sqlite3.Error, pd.errors.DatabaseError) as error:
    st.error(f"Unable to read clern_weather: {error}")
    st.stop()

# -----------------------------
# Dashboard Layout
# -----------------------------
st.set_page_config(page_title="World Weather Dashboard", layout="wide")
st.title("🌎 Weather Around the World Dashboard")
st.write("Explore global weather patterns using interactive visualizations. Use the filters to update all charts.")
st.caption("This dashboard shows saved observations, not a live weather feed.")


# -----------------------------
# Filters
# -----------------------------

# Custom CSS to modify sidebar width
st.markdown(
    """
    <style>
    .st-emotion-cache-197vr8o {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
    }
    .st-emotion-cache-119tkyc {
        color: rgb(49, 51, 63);
        font-size: 1em;
        font-weight: 400;
    }
    .stSlider {
        width: 400px; /* Change this to your desired width */
    }
    </style>
    """,
    unsafe_allow_html=True
)

df["temperature_c"] = pd.to_numeric(df["temperature_c"], errors="coerce")
df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce", utc=True)
latest = df["scraped_at"].max()

st.sidebar.header("Explore Weather")
countries = sorted(df["country"].unique())
selected_country = st.sidebar.selectbox("Select a country", countries, index=2)

unit = st.sidebar.selectbox("Temperature Unit", ["Celsius", "Fahrenheit"])
df["temperature_column"] = df["temperature_c"] if unit == "Celsius" else df["temperature_c"] * 9 / 5 + 32
df["temperature_column"] = pd.to_numeric(df["temperature_column"], errors="coerce")
unit_label = "°C" if unit == "Celsius" else "°F"

filtered = df[
    (df["country"] == selected_country) & df["condition"] & df["temperature_column"]  
].copy()
if filtered.empty:
    st.warning("No observations match these filters. Select more countries or conditions, or widen the temperature range.")
    st.stop()

col1, col2 = st.columns(2)
with col1:
    temp_value = filtered["temperature_column"].iloc[0]
    st.write("Country Temperature")
    st.write(temp_value, unit_label)
    
with col2:
    condition = filtered["condition"].iloc[0]
    st.write("Weather Condition")
    st.write(condition)
    
labels = {"temperature_column": f"Temperature ({unit_label})", "country": "Country", "condition": "Weather Condition", "count": "Observations"}

# -----------------------------
# Visualization 1: Top Cities by Temperature (Bar Chart)
# -----------------------------
st.subheader("Top Cities by Temperature")

top_n = st.slider("Number of cities to display", 5, 20, 10)
top_cities = filtered.nlargest(top_n, "temperature_column")

fig2 = px.bar(
    top_cities,
    x="city",
    y="temperature_column",
    color="temperature_column",
    title=f"Top {top_n} Hottest Cities in {selected_country}",
    labels={"city": "City", "temperature_column": "Temperature"},
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Visualization 2: Temperature Distribution (Histogram)
# -----------------------------
st.subheader("Temperature Distribution")
fig1 = px.histogram(
        filtered,
        x="temperature_column",
        nbins=20,
        title=f"Temperature Distribution in {selected_country}",
        labels={"temperature_column": "Temperature"},
    )
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Visualization 3: Compare Countries (Scatter Plot)
# -----------------------------
st.subheader("Compare Countries")
compare_countries = st.multiselect(
    "Select countries to compare",
    countries,
    default=[selected_country]
)

compare_df = df[df["country"].isin(compare_countries)]

fig3 = px.scatter(
    compare_df,
    x="city",
    y="temperature_c",
    color="country",
    size="temperature_c",
    hover_name="city",
    title="Temperature Comparison Across Countries",
    labels={"city": "City", "temperature_c": "Temperature", "country": "Country"},
)
st.plotly_chart(fig3, use_container_width=True)

st.write("Use the filters above to explore the dataset.")