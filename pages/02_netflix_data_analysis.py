# The libraries you have to use
import pandas as pd
import matplotlib.pyplot as plt

# Some extra libraries to build the webapp
import streamlit as st


# ----- Left menu -----
with st.sidebar:
    st.image("eae_img.png", width=200)
    st.write("Interactive Project to load a dataset with information about Netflix Movies and Series, extract some insights usign Pandas and displaying them with Matplotlib.")
    st.write("Data extracted from: https://www.kaggle.com/datasets/shivamb/netflix-shows (with some cleaning and modifications)")


# ----- Title of the page -----
st.title("🎬 Netflix Data Analysis")
st.divider()


# ----- Loading the dataset -----

@st.cache_data
def load_data():
    data_path = "data/netflix_titles.csv"

    movies_df = pd.read_csv(data_path, index_col="show_id")  # TODO: Ex 2.1: Load the dataset using Pandas, use the data_path variable and set the index column to "show_id"

    # Ex 2.1: Load the data using Pandas read_csv, use `show_id` as the index_col parameter. 

    # Returning the loaded dataframe

    return movies_df   # a Pandas DataFrame


movies_df = load_data()

# Displaying the dataset in a expandable table
with st.expander("Check the complete dataset:"):
    st.dataframe(movies_df)


# ----- Extracting some basic information from the dataset -----

# TODO: Ex 2.2: What is the min and max release years?
min_year = movies_df["release_year"].min()  # TODO: Ex 2.2: Minimum release year
max_year = movies_df["release_year"].max()  # TODO: Ex 2.2: Maximum release year

# TODO: Ex 2.3: How many director names are missing values (NaN)?
num_missing_directors = movies_df["director"].isna().sum()  # TODO: Ex 2.3: Number of missing director names

# TODO: Ex 2.4: How many different countries are there in the data?
countries_filled = movies_df["country"].fillna("Unknown")
country_lists = countries_filled.apply(lambda x: x.split(", "))
all_countries = [country for sublist in country_lists for country in sublist]
unique_countries = set(all_countries)
n_countries = len(unique_countries)

# TODO: Ex 2.5: How many characters long are on average the title names?
movies_df["title_length"] = movies_df["title"].apply(lambda x: len(x))
avg_title_length = movies_df["title_length"].mean()  # TODO

# ----- Displaying the extracted information metrics -----

st.write("##")
st.header("Basic Information")

cols1 = st.columns(5)
cols1[0].metric("Min Release Year", min_year)
cols1[1].metric("Max Release Year", max_year)
cols1[2].metric("Missing Dir. Names", num_missing_directors)
cols1[3].metric("Countries", n_countries)
cols1[4].metric("Avg Title Length", str(round(avg_title_length, 2)) if avg_title_length is not None else None)


# ----- Pie Chart: Top year producer countries -----

st.write("##")
st.header("Top Year Producer Countries")

cols2 = st.columns(2)
year = cols2[0].number_input("Select a year:", min_year, max_year, 2005)

# TODO: Ex 2.6: For a given year, get the Pandas Series of how many movies and series 
# combined were made by every country, limit it to the top 10 countries.
df_year = movies_df.loc[movies_df["release_year"] == year]
top_10_countries =  df_year["country"].value_counts().head(10) # TODO: top_10_countries has to be a Pandas Series with the top 10 countries with the number of movies and series combined for that year

# print(top_10_countries)
if top_10_countries is not None:
    fig = plt.figure(figsize=(8, 8))
    plt.pie(top_10_countries, labels=top_10_countries.index, autopct="%.2f%%")
    plt.title(f"Top 10 Countries in {year}")

    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.6.")


# ----- Line Chart: Avg duration of movies by year -----

st.write("##")
st.header("Avg Duration of Movies by Year")

# TODO: Ex 2.7: Make a line chart of the average duration of movies (not TV shows) in minutes for every year across all the years. 
movies_only = movies_df[movies_df["type"] == "Movie"]

movies_only["duration_minutes"] = movies_only["duration"].apply(
    lambda x: int(x.split(" ")[0])
)

movies_avg_duration_per_year = movies_only.groupby("release_year")["duration_minutes"].mean()

if movies_avg_duration_per_year is not None:
    fig = plt.figure(figsize=(9, 6))
    plt.plot(movies_avg_duration_per_year.index, movies_avg_duration_per_year.values)
    plt.xlabel("Year")
    plt.ylabel("Average Duration (minutes)")
    plt.title("Average Duration of Movies Across Years")
    plt.grid(True)
    plt.show()    
    st.pyplot(fig)

else:
    st.subheader("⚠️ You still need to develop the Ex 2.7.")

