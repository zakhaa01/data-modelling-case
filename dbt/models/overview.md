{% docs __overview__ %}

# Data Documentation TMDB movies details

## Objective
The goal of this dbt project is to transform raw movie-related data into clean, structured datasets that facilitate analytical insights.

## Key Features

* Data Cleaning & Standardization: Removes duplicates, standardizes column names, and ensures consistency across datasets.

* Aggregations & Calculations:

    - Calculates average movie ratings.

    - Aggregates genres into lists per movie.

    - Counts movie appearances per actor.

* Join Optimizations: Efficiently combines multiple sources to produce meaningful insights.

{% enddocs %}
