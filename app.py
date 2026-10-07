import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="TMDB Movie Analysis",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🎬 TMDB 5000 Movie Data Analysis")
st.markdown(
    "An interactive dashboard for exploring movies, ratings, "
    "popularity, genres, revenue, budget, and directors."
)

st.divider()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("tmdb_merged_movie_data.csv")
    return df


try:
    df = load_data()

except FileNotFoundError:
    st.error(
        "tmdb_final_cleaned.csv was not found. "
        "Please keep the CSV file in the same folder as app.py."
    )
    st.stop()

# ---------------------------------------------------------
# BASIC CLEANING
# ---------------------------------------------------------

# Convert numeric columns if they exist
numeric_columns = [
    "budget",
    "revenue",
    "popularity",
    "runtime",
    "vote_average",
    "vote_count"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

# Convert release date
if "release_date" in df.columns:
    df["release_date"] = pd.to_datetime(
        df["release_date"],
        errors="coerce"
    )

    df["release_year"] = df["release_date"].dt.year

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

st.sidebar.header("🎯 Filters")

filtered_df = df.copy()

# Genre filter
if "primary_genre" in df.columns:

    genres = sorted(
        df["primary_genre"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_genres = st.sidebar.multiselect(
        "Select Genre",
        genres
    )

    if selected_genres:
        filtered_df = filtered_df[
            filtered_df["primary_genre"].isin(selected_genres)
        ]

# Language filter
if "original_language" in df.columns:

    languages = sorted(
        df["original_language"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_languages = st.sidebar.multiselect(
        "Select Language",
        languages
    )

    if selected_languages:
        filtered_df = filtered_df[
            filtered_df["original_language"].isin(selected_languages)
        ]

# Release year filter
if "release_year" in filtered_df.columns:

    years = filtered_df["release_year"].dropna()

    if len(years) > 0:

        min_year = int(years.min())
        max_year = int(years.max())

        if min_year < max_year:

            year_range = st.sidebar.slider(
                "Release Year",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )

            filtered_df = filtered_df[
                filtered_df["release_year"].between(
                    year_range[0],
                    year_range[1]
                )
            ]

# Rating filter
if "vote_average" in filtered_df.columns:

    rating_range = st.sidebar.slider(
        "Minimum / Maximum Rating",
        min_value=0.0,
        max_value=10.0,
        value=(0.0, 10.0),
        step=0.1
    )

    filtered_df = filtered_df[
        filtered_df["vote_average"].between(
            rating_range[0],
            rating_range[1]
        )
    ]

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Movies",
        f"{len(filtered_df):,}"
    )

with col2:

    if "vote_average" in filtered_df.columns:
        avg_rating = filtered_df["vote_average"].mean()

        st.metric(
            "Average Rating",
            f"{avg_rating:.2f}"
        )
    else:
        st.metric("Average Rating", "N/A")

with col3:

    if "popularity" in filtered_df.columns:
        avg_popularity = filtered_df["popularity"].mean()

        st.metric(
            "Average Popularity",
            f"{avg_popularity:.2f}"
        )
    else:
        st.metric("Average Popularity", "N/A")

with col4:

    if "revenue" in filtered_df.columns:
        total_revenue = filtered_df["revenue"].sum()

        st.metric(
            "Total Revenue",
            f"${total_revenue:,.0f}"
        )
    else:
        st.metric("Total Revenue", "N/A")


st.divider()

# ---------------------------------------------------------
# TOP MOVIES
# ---------------------------------------------------------

st.subheader("🏆 Top Movies")

top_col1, top_col2 = st.columns(2)

with top_col1:

    if "popularity" in filtered_df.columns:

        title_column = (
            "title"
            if "title" in filtered_df.columns
            else None
        )

        if title_column:

            top_popular = filtered_df.sort_values(
                "popularity",
                ascending=False
            ).head(10)

            fig = px.bar(
                top_popular.sort_values("popularity"),
                x="popularity",
                y="title",
                orientation="h",
                title="Top 10 Most Popular Movies",
                labels={
                    "popularity": "Popularity",
                    "title": "Movie"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

with top_col2:

    if "vote_average" in filtered_df.columns:

        title_column = (
            "title"
            if "title" in filtered_df.columns
            else None
        )

        if title_column:

            top_rated = filtered_df[
                filtered_df["vote_count"].fillna(0) >= 100
            ].sort_values(
                "vote_average",
                ascending=False
            ).head(10)

            fig = px.bar(
                top_rated.sort_values("vote_average"),
                x="vote_average",
                y="title",
                orientation="h",
                title="Top Rated Movies",
                labels={
                    "vote_average": "Rating",
                    "title": "Movie"
                }
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# ---------------------------------------------------------
# GENRE ANALYSIS
# ---------------------------------------------------------

if "primary_genre" in filtered_df.columns:

    st.subheader("🎭 Genre Analysis")

    genre_count = (
        filtered_df["primary_genre"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = [
        "Genre",
        "Movie Count"
    ]

    fig = px.bar(
        genre_count.head(15),
        x="Genre",
        y="Movie Count",
        title="Movies by Genre"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# RELEASE YEAR TREND
# ---------------------------------------------------------

if "release_year" in filtered_df.columns:

    st.subheader("📅 Movie Release Trend")

    yearly_movies = (
        filtered_df
        .dropna(subset=["release_year"])
        .groupby("release_year")
        .size()
        .reset_index(name="Movie Count")
    )

    fig = px.line(
        yearly_movies,
        x="release_year",
        y="Movie Count",
        markers=True,
        title="Number of Movies Released by Year",
        labels={
            "release_year": "Release Year"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------------
# RATING VS POPULARITY
# ---------------------------------------------------------

if "vote_average" in filtered_df.columns and \
   "popularity" in filtered_df.columns:

    st.subheader("⭐ Rating vs Popularity")

    scatter_df = filtered_df.dropna(
        subset=[
            "vote_average",
            "popularity"
        ]
    )

    if len(scatter_df) > 0:

        fig = px.scatter(
            scatter_df,
            x="vote_average",
            y="popularity",
            hover_name="title" if "title" in scatter_df.columns else None,
            size="vote_count"
            if "vote_count" in scatter_df.columns
            else None,
            title="Relationship Between Rating and Popularity",
            labels={
                "vote_average": "Rating",
                "popularity": "Popularity"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------------------------
# BUDGET VS REVENUE
# ---------------------------------------------------------

if "budget" in filtered_df.columns and \
   "revenue" in filtered_df.columns:

    st.subheader("💰 Budget vs Revenue")

    revenue_df = filtered_df[
        (filtered_df["budget"] > 0) &
        (filtered_df["revenue"] > 0)
    ]

    if len(revenue_df) > 0:

        fig = px.scatter(
            revenue_df,
            x="budget",
            y="revenue",
            hover_name="title"
            if "title" in revenue_df.columns
            else None,
            title="Movie Budget vs Revenue",
            labels={
                "budget": "Budget ($)",
                "revenue": "Revenue ($)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------------------------
# RUNTIME DISTRIBUTION
# ---------------------------------------------------------

if "runtime" in filtered_df.columns:

    st.subheader("⏱️ Movie Runtime Distribution")

    runtime_df = filtered_df.dropna(
        subset=["runtime"]
    )

    runtime_df = runtime_df[
        runtime_df["runtime"] > 0
    ]

    if len(runtime_df) > 0:

        fig = px.histogram(
            runtime_df,
            x="runtime",
            nbins=30,
            title="Distribution of Movie Runtime",
            labels={
                "runtime": "Runtime (minutes)"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------------------------
# DIRECTOR ANALYSIS
# ---------------------------------------------------------

if "director" in filtered_df.columns:

    st.subheader("🎥 Director Analysis")

    director_count = (
        filtered_df[
            filtered_df["director"].notna()
        ]
        .query("director != 'Unknown'")
        ["director"]
        .value_counts()
        .reset_index()
        .head(15)
    )

    director_count.columns = [
        "Director",
        "Movie Count"
    ]

    if len(director_count) > 0:

        fig = px.bar(
            director_count.sort_values("Movie Count"),
            x="Movie Count",
            y="Director",
            orientation="h",
            title="Directors with the Most Movies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# ---------------------------------------------------------
# MOVIE DATA TABLE
# ---------------------------------------------------------

st.subheader("🎬 Movie Dataset")

display_columns = [
    "title",
    "release_year",
    "primary_genre",
    "director",
    "vote_average",
    "popularity",
    "runtime",
    "budget",
    "revenue"
]

available_columns = [
    column
    for column in display_columns
    if column in filtered_df.columns
]

if available_columns:

    st.dataframe(
        filtered_df[available_columns].sort_values(
            "popularity",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.markdown(
    """
    **TMDB 5000 Movie Analysis**  
    Developed using Python, Pandas, Plotly and Streamlit.
    """
)
