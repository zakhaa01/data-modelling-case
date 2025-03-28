"""
    Written by: zakhaa01
    Python data extraction script to fetch TMDB movie details through API calls.
"""
# pylint: disable=unused-import
import os
import logging
from datetime import datetime, timezone
import sqlalchemy as sa
import psycopg2
import pandas as pd
import requests

# Logger config
log = logging.getLogger(__name__)
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
log.addHandler(sh)
log.setLevel(logging.DEBUG)

# Globals
ENV: str = os.getenv("ENV", None)
USERNAME: str = os.getenv("TMDB_USERNAME", None)
PASSWORD: str = os.getenv("TMDB_PASSWORD", None)
HOST: str = os.getenv("TMDB_HOST", None)
API_KEY: str = os.getenv("TMDB_API_KEY", None)
DEFAULT_SCHEMA: str = os.getenv("DEFAULT_SCHEMA", None)
DB_CONFIG: dict = {
    "user": USERNAME,
    "password": PASSWORD,
    "host": HOST,
    "port": 5432,
    "dbname": f"{ENV}_tmdb_dwh",
}
BASE_URL: str = "https://api.themoviedb.org/3/movie"
HEADERS: dict = {"accept": "application/json", "Authorization": API_KEY}
LANGUAGE: str = "language=en-US"
SCHEMA_RAW: str = f"{DEFAULT_SCHEMA}_raw"


def get_engine() -> sa.engine.base.Engine:
    """Create a SQLAlchemy engine."""
    db_url = (
        f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    )
    engine = sa.create_engine(db_url)
    log.info("Engine created.")
    return engine


def api_request(url: str) -> dict:
    """Create API call."""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()


def get_top_rated_movies(pages: int = 1) -> list:
    """
    Fetch the first page of top-rated movies ids.
    Args:
        pages (int): Number of pages to fetch (default is 1).

    Returns:
        list: A list of movie IDs for top-rated movies.
    """
    movie_ids = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}/top_rated?{LANGUAGE}&page={page}"
        top_movies = api_request(url)
        log.info("%s page top movies API request done.", page)
        movie_ids.extend(movie["id"] for movie in top_movies.get("results", []))
    log.info("Top rated movies list created.")
    return movie_ids


def get_details(movie_id: int) -> dict:
    """
    Fetch movie details.
    Args:
        movie_id (int): Movie id to look for movie details.

    Returns:
        Dictionary with movie details data.
    """
    url = f"{BASE_URL}/{movie_id}?{LANGUAGE}"
    details_data = api_request(url)
    log.info("%s movie id details API call done.", movie_id)
    return details_data


def get_credits(movie_id: int) -> dict:
    """
    Fetch movie credits.
    Args:
        movie_id (int): Movie id to look for credits.

    Returns:
        Dictionary with credits data.
    """
    url = f"{BASE_URL}/{movie_id}/credits?{LANGUAGE}"
    credits_data = api_request(url)
    log.info("%s movie id credits API call done.", movie_id)
    return credits_data


def get_similar(movie_id: int) -> dict:
    """
    Fetch similar movies.
    Args:
        movie_id (int): Movie id to look for similar movies.

    Returns:
        Dictionary with similar movies data.
    """
    url = f"{BASE_URL}/{movie_id}/similar?{LANGUAGE}"
    similar_data = api_request(url)
    log.info("%s similar movies API call done.", movie_id)
    return similar_data


def write_df_to_postgresql(
    engine: sa.engine.base.Engine,
    table_name: str,
    df: pd.DataFrame,
    schema: str = SCHEMA_RAW,
    if_exists: str = "append",
) -> None:
    """
    Insert data into a PostgreSQL table using pandas.

    Args:
        engine: SQLAlchemy engine instance.
        table_name (str): Name of the table to insert data into.
        df (pd.DataFrame): Dataframe to be inserted.
        schema (str): Name of the schema where the table is located.
        if_exists (str): Behavior when the table exists ('fail', 'replace', 'append').

    Returns:
        None
    """
    # Write to database
    with engine.begin() as connection:
        df.to_sql(
            table_name, connection, schema=schema, if_exists=if_exists, index=False
        )

    log.info("%s successfully loaded to PostgreSQL.", df)


def process_tmdb_data(  # pylint: disable=too-many-locals
    engine: sa.engine.base.Engine,
    movie_ids: list,
    table_name: str,
    table_config: dict,
) -> None:
    """
    Process raw DataFrames and loat them to PostgreSQL.

    Args:
        engine: SQLAlchemy engine instance.
        movie_ids (list): A list of movie IDs for top-rated movies.
        table_name (str): Name of the table to insert data into.
        table_config (dict): A dictionary with additional information for DataFrames.

    Returns:
        None
    """
    response_data_raw: list = []  # empty placeholder list creation
    get_data_func: function = table_config[  # pylint: disable=undefined-variable
        "getter_func"
    ]
    field_mapping: dict = table_config["field_mapping"]
    nested_field: str = table_config["nested_field"]
    limitation: int = table_config["slice"]
    for movie_id in movie_ids:  # loop through `movie_ids`
        api_record = get_data_func(movie_id)  # table_type-specific getter function
        nested_values = (
            api_record[nested_field][:limitation] if nested_field else [api_record]
        )

        for entity in nested_values:
            row_record = {
                "movie_id": movie_id,
                "extracted_at_utc": datetime.now(timezone.utc),
            }
            for column, field in field_mapping.items():
                row_record[column] = entity[field]
            response_data_raw.append(row_record)

    df = pd.DataFrame(response_data_raw)  # turn dict to DF
    log.info("DataFrame for %s created.", table_name)  # logging success
    write_df_to_postgresql(engine, table_name, df)  # write to db


def main():
    """Main process"""

    tables_config = {
        "movies": {
            "getter_func": get_details,
            "slice": None,
            "nested_field": None,
            "field_mapping": {
                "title": "title",
                "country_code": "origin_country",
                "tagline": "tagline",
                "overview": "overview",
                "release_date": "release_date",
                "popularity": "popularity",
                "rating_avg": "vote_average",
                "vote_count": "vote_count",
                "budget_usd": "budget",
                "revenue_usd": "revenue",
            },
        },
        "movies_genre": {
            "getter_func": get_details,
            "slice": None,
            "nested_field": "genres",
            "field_mapping": {
                "genre_id": "id",
                "genre_name": "name",
            },
        },
        "credits": {
            "getter_func": get_credits,
            "slice": 10,
            "nested_field": "cast",
            "field_mapping": {
                "actor_id": "id",
                "actor_name": "name",
                "character_name": "character",
            },
        },
        "similar": {
            "getter_func": get_similar,
            "slice": 5,
            "nested_field": "results",
            "field_mapping": {
                "similar_movie_id": "id",
                "similar_movie_name": "title",
            },
        },
    }

    log.info("START: TMDB data processing initiated...")

    engine = get_engine()
    movie_ids = get_top_rated_movies(pages=50)

    for table_name, table_config in tables_config.items():
        process_tmdb_data(engine, movie_ids, table_name, table_config)

    log.info("OK: Data is processed and uploaded to database!")


if __name__ == "__main__":
    main()
