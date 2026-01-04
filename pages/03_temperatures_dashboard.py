# the libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries for date conversions and build the webapp
import streamlit as st
import os


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write(
        "Interactive Project to load a dataset with information about the daily temperatures of 10 cities around the world, "
        "extract some insights using Pandas and displaying them with Matplotlib."
    )
    st.write(
        "Data extracted from: https://www.kaggle.com/datasets/sudalairajkumar/daily-temperature-of-major-cities "
        "(with some cleaning and modifications)."
    )


# ----- Title of the page -----
st.title("🌦️ Temperatures Dashboard")
st.divider()


# ----- Loading the dataset -----
@st.cache_data
def load_data():

    data_path = "data/cities_temperatures.csv"

    temps_df = pd.read_csv(data_path, index_col="Country")

    if "Date" in temps_df.columns:
        temps_df["Date"] = pd.to_datetime(temps_df["Date"]).dt.date

    return temps_df


temps_df = load_data()

# Displaying the dataset in an expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(temps_df)


# ----- Data transformation -----
# Ex 3.2: Create a new column called AvgTemperatureCelsius
if "AvgTemperatureCelsius" not in temps_df.columns:
    temps_df.insert(
        temps_df.columns.get_loc("AvgTemperatureFahrenheit") + 1,
        "AvgTemperatureCelsius",
        (temps_df["AvgTemperatureFahrenheit"] - 32) * 5 / 9
    )


# ----- Extracting some basic information from the dataset -----
# Ex 3.3: How many different cities are there? Provide a list of them.
unique_cities_list = temps_df["City"].dropna().unique().tolist()

# Ex 3.4: Which are the minimum and maximum dates?
min_date = temps_df["Date"].min()
max_date = temps_df["Date"].max()

# Ex 3.5: Global min and max temperatures + city + date
min_country = temps_df["AvgTemperatureCelsius"].idxmin()
max_country = temps_df["AvgTemperatureCelsius"].idxmax()

min_row = temps_df.loc[min_country]
max_row = temps_df.loc[max_country]

if isinstance(min_row, pd.DataFrame):
    min_row = min_row.iloc[0]
if isinstance(max_row, pd.DataFrame):
    max_row = max_row.iloc[0]

min_temp = float(min_row["AvgTemperatureCelsius"])
min_temp_city = min_row["City"]
min_temp_date = min_row["Date"]

max_temp = float(max_row["AvgTemperatureCelsius"])
max_temp_city = max_row["City"]
max_temp_date = max_row["Date"]


# ----- Displaying the extracted information metrics -----
st.write("##")
st.header("Basic Information")

cols1 = st.columns([4, 1, 6])

# Cities list
if unique_cities_list is not None:
    cols1[0].dataframe(pd.Series(unique_cities_list, name="Cities"), width="content")
else:
    cols1[0].write("⚠️ You still need to develop the Ex 3.3.")

# Min / Max block
if min_date is not None and max_date is not None:
    cols1[2].write("#")

    min_temp_text = f"""
    ### ☃️ Min Temperature: {min_temp:.1f}°C
    *{min_temp_city} on {min_temp_date}*
    """
    cols1[2].write(min_temp_text)

    cols1[2].write("#")

    max_temp_text = f"""
    ### 🏜️ Max Temperature: {max_temp:.1f}°C
    *{max_temp_city} on {max_temp_date}*
    """
    cols1[2].write(max_temp_text)
else:
    cols1[2].write("⚠️ You still need to develop the Ex 3.5.")


# ----- Plotting the temperatures over time for the selected cities -----
st.write("##")
st.header("Comparing the Temperatures of the Cities")

if unique_cities_list is not None:
    # Getting the list of cities to compare from the user
    selected_cities = st.multiselect(
        "Select the cities to compare:",
        unique_cities_list,
        default=["Buenos Aires", "Dakar"],
        max_selections=4
    )

    cols2 = st.columns([6, 1, 6])
    start_date = cols2[0].date_input("Select the start date:", pd.to_datetime("2009-01-01").date())
    end_date = cols2[2].date_input("Select the end date:", pd.to_datetime("2018-12-31").date())

else:
    st.subheader("⚠️ You still need to develop the Ex 3.3.")
    selected_cities = []


if unique_cities_list is not None and len(selected_cities) > 0:

    c = st.container(border=True)

    # ----- Ex 3.7: Line plot (one line per city) -----
    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:
        city_df = temps_df[temps_df["City"] == city]

        city_df_period = city_df[
            (city_df["Date"] >= start_date) &
            (city_df["Date"] <= end_date)
        ]

        plt.plot(
            city_df_period["Date"],
            city_df_period["AvgTemperatureCelsius"],
            label=city
        )

    plt.title("Average temperature by city")
    plt.xlabel("Date")
    plt.ylabel("Average temperature (°C)")
    plt.legend()

    c.pyplot(fig)

    # ----- Histogram (one distribution per city) -----
    fig = plt.figure(figsize=(10, 5))

    for city in selected_cities:
        city_df = temps_df[temps_df["City"] == city]

        city_df_period = city_df[
            (city_df["Date"] >= start_date) &
            (city_df["Date"] <= end_date)
        ]

        plt.hist(
            city_df_period["AvgTemperatureCelsius"].dropna(),
            bins=20,
            alpha=0.5,
            label=city
        )

    plt.title("Temperature Distribution by City (selected period)")
    plt.xlabel("Average Temperature (°C)")
    plt.ylabel("Frequency")
    plt.legend()

    c.pyplot(fig)

else:
    st.info("Select at least one city to display the plots.")
