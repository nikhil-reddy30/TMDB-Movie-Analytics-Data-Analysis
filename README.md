# 🎬 TMDB Movie Analytics & Data Analysis

## 📌 Project Overview

This project performs an end-to-end **data analysis of movies from the TMDB 5000 dataset**. The analysis combines movie information with credits data to explore movie performance, revenue, budget, ratings, popularity, genres, directors, and trends over time.

The project includes:

* Data loading and inspection
* Data quality assessment
* Data cleaning and preprocessing
* Feature engineering
* Merging multiple datasets
* Exploratory Data Analysis (EDA)
* Interactive visualizations using Plotly
* KPI analysis
* Movie performance analysis
* Interactive HTML dashboard
* Exporting processed datasets and analytical summaries

---

## 🎯 Objectives

The main objectives of this project are to:

1. Analyze movie budgets and revenues.
2. Identify the highest-grossing movies.
3. Analyze revenue performance by genre.
4. Study movie trends over the years.
5. Analyze directors based on movie performance.
6. Examine the relationship between budget and revenue.
7. Compare successful and unsuccessful movies.
8. Analyze the relationship between ratings and popularity.
9. Study average movie ratings across decades.
10. Create an interactive movie analytics dashboard.

---

## 📂 Dataset

The project uses two CSV files from the **TMDB 5000 Movie Dataset**:

### 1. `tmdb_5000_movies.csv`

Contains movie-level information such as:

* Movie ID
* Title
* Budget
* Revenue
* Popularity
* Vote Average
* Vote Count
* Release Date
* Runtime
* Genres
* Original Language
* Status

### 2. `tmdb_5000_credits.csv`

Contains movie credit information including:

* Movie ID
* Cast
* Crew

The two datasets are connected using the movie ID.

---

## 🗂️ Project Structure

```text
TMDB-Movie-Analytics/
│
├── project/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
├── output/
│   ├── tmdb_merged_movie_data.csv
│   ├── genre_summary.csv
│   ├── yearly_summary.csv
│   ├── director_summary.csv
│   ├── quality_report.csv
│   └── movie_dashboard.html
│
├── mini_project.ipynb
└── README.md
```

---

## 🛠️ Technologies Used

* **Python**
* **Pandas** – Data manipulation and analysis
* **NumPy** – Numerical operations
* **Plotly Express** – Interactive visualizations
* **Plotly Graph Objects** – Dashboard creation
* **Jupyter Notebook / Google Colab**

---

## 🔄 Project Workflow

### 1. Data Loading

The project loads the two TMDB datasets using Pandas:

```python
movies = pd.read_csv("project/tmdb_5000_movies.csv")
credits = pd.read_csv("project/tmdb_5000_credits.csv")
```

Both datasets are inspected for their:

* Shape
* Columns
* Data types
* Unique IDs
* Duplicate records
* Missing values

---

### 2. Data Quality Analysis

Several data quality checks were performed, including:

* Missing-value analysis
* Duplicate-row checks
* Duplicate movie ID checks
* Negative budget checks
* Negative revenue checks
* Negative runtime checks
* Invalid release-date checks
* ID matching between the two datasets

This ensures that the datasets are suitable for further analysis.

---

### 3. Data Cleaning & Preprocessing

The `release_date` column was converted into a proper datetime format.

A new feature called `release_year` was created from the release date.

Relevant movie columns were selected for the analysis to create a more focused analytical dataset.

---

## 🧮 Feature Engineering

Several new analytical features were created.

### Profit

```text
Profit = Revenue - Budget
```

### ROI

ROI was calculated only when the movie had a positive budget:

```text
ROI = (Revenue - Budget) / Budget
```

### Financial Features

The following values were converted into millions:

* Budget
* Revenue
* Profit

### Rating Groups

Movies were categorized into:

| Rating | Group     |
| ------ | --------- |
| ≤ 5    | Low       |
| 5–7    | Average   |
| 7–8    | Good      |
| > 8    | Excellent |

### Release Decade

The release year was transformed into a decade-based feature.

### Successful Movie

A movie was considered successful when:

```text
Revenue > Budget
AND
Budget > 0
```

---

## 🎭 Genre & Director Extraction

The project extracts:

* **Primary genre** from the genres column
* **Director** from the crew information

Missing director values were replaced with:

```text
unknown
```

Missing primary genres were replaced with:

```text
unknown
```

Missing runtime values were filled using the **median runtime**.

---

## 🔗 Dataset Merging

The movies and credits datasets were merged using their movie IDs.

```python
merged_df = movies_selected.merge(
    credits_selected,
    left_on="id",
    right_on="movie_id",
    how="left",
    validate="one_to_one"
)
```

The merged dataset was then validated to ensure:

* Movie count remained consistent
* Movie IDs remained unique
* Titles were available
* Budget and revenue were non-negative
* Ratings were within the expected range

---

## 📊 Exploratory Data Analysis

The project performs analysis on several important business questions.

### 💰 Revenue by Genre

The project calculates:

* Number of movies
* Average budget
* Average revenue
* Average rating
* Total revenue

for each primary genre.

### 🏆 Top-Grossing Movies

The top 10 movies based on revenue are identified along with:

* Genre
* Budget
* Revenue
* Profit
* Rating
* Director

### 📅 Movie Trends by Year

Movie performance is analyzed over release years using:

* Number of movies
* Average budget
* Average revenue
* Average rating
* Total revenue

### 🎬 Director Analysis

Directors with at least three movies are analyzed based on:

* Number of movies
* Average revenue
* Average rating
* Total revenue

### 📈 Budget vs Revenue

The relationship between movie budget and revenue is analyzed using correlation and an interactive scatter plot.

### ⭐ Rating vs Popularity

The project explores the relationship between:

* Average rating
* Popularity
* Number of votes

### 🏅 Successful vs Unsuccessful Movies

Movies are grouped according to whether they generated more revenue than their budget.

The groups are compared based on:

* Number of movies
* Average budget
* Average revenue
* Average rating
* Average popularity

---

## 📈 Visualizations

The project contains interactive Plotly visualizations including:

### 1. Average Revenue by Primary Genre

Shows how average movie revenue differs across genres.

### 2. Budget vs Revenue

A scatter plot comparing movie budgets and revenues.

### 3. Total Revenue by Release Year

Shows movie revenue trends across release years.

### 4. Top 10 Movies by Revenue

Displays the highest-revenue movies.

### 5. Rating vs Popularity

Shows the relationship between movie ratings and popularity.

### 6. Average Rating by Release Decade

Shows how average movie ratings vary across different decades.

---

## 📊 Interactive Dashboard

An interactive **TMDB Movie Analytics Dashboard** was created using Plotly.

The dashboard contains:

* Average Revenue by Genre
* Budget vs Revenue
* Top 10 Movies by Revenue
* Average Rating by Decade

The dashboard is exported as:

```text
output/movie_dashboard.html
```

You can open the HTML file directly in a web browser.

---

## 📁 Output Files

The project exports the following analytical files:

| File                         | Description                     |
| ---------------------------- | ------------------------------- |
| `tmdb_merged_movie_data.csv` | Final merged analytical dataset |
| `genre_summary.csv`          | Genre-level analysis            |
| `yearly_summary.csv`         | Year-wise movie analysis        |
| `director_summary.csv`       | Director-level analysis         |
| `quality_report.csv`         | Data quality report             |
| `movie_dashboard.html`       | Interactive Plotly dashboard    |

---

## 📌 Key KPIs

The project calculates the following KPIs:

* **Total Movies**
* **Total Revenue ($B)**
* **Average Rating**
* **Number of Positive ROI Movies**

These KPIs provide a quick overview of the movie dataset and its financial performance.

---

## 🚀 How to Run the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/your-username/TMDB-Movie-Analytics.git
```

### Step 2: Navigate to the project

```bash
cd TMDB-Movie-Analytics
```

### Step 3: Install required libraries

```bash
pip install pandas numpy plotly jupyter
```

### Step 4: Start Jupyter Notebook

```bash
jupyter notebook
```

### Step 5: Open

```text
mini_project.ipynb
```

Make sure the dataset files are located inside:

```text
project/
```

---

## 💡 Business Questions Answered

This project helps answer questions such as:

* Which movie genres generate higher average revenue?
* Which movies have the highest revenue?
* Does a higher budget generally lead to higher revenue?
* Which directors have generated the highest total revenue?
* How has movie revenue changed over time?
* How do successful movies differ from unsuccessful movies?
* Is movie popularity related to rating?
* How have average movie ratings changed across decades?

---

## 🔍 Key Learning Outcomes

Through this project, I practiced:

* Real-world dataset handling
* Data cleaning
* Missing-value treatment
* Data validation
* Feature engineering
* Dataset merging
* Exploratory Data Analysis
* Statistical correlation analysis
* Interactive data visualization
* Dashboard development
* Exporting analytical datasets
* Communicating data-driven insights

---

## 👨‍💻 Author

**Nikhil**

Aspiring Data Analyst | Data Scientist | Machine Learning Enthusiast

### Skills Demonstrated

`Python` `Pandas` `NumPy` `Plotly` `Data Cleaning` `EDA` `Feature Engineering` `Data Visualization` `Dashboard Development`

---

## ⭐ Project Highlights

This project demonstrates an end-to-end data analytics workflow:

```text
Raw Data
   ↓
Data Quality Check
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Dataset Merging
   ↓
Validation
   ↓
EDA
   ↓
Visualization
   ↓
Dashboard
   ↓
Exported Analytical Data
```

---

## 📜 Dataset Reference

The project uses the TMDB 5000 Movies and Credits datasets for educational and analytical purposes.
