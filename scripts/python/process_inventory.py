"""
    Written by: zakhaa01
    ETL Python-Pandas script to process music inventory db
    and write data analytic plots.
"""
import os
import logging
from typing import Literal

import sqlite3 as sq
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

# Logger config
log = logging.getLogger(__name__)
sh = logging.StreamHandler()
sh.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
log.addHandler(sh)
log.setLevel(logging.DEBUG)

# Various Globals
PLOTS_PATH: str = "./output/plots/"
CONN_URL: str = os.getenv("music_db_conn_url", None)
TABLE_NAMES: list = ["Track", "Album", "Genre", "InvoiceLine"]


def read_data_from_db(connection, table_names) -> dict:
    """
    Reads tables from database.

    Args:
        connection: The database connection object.
        table_names: A list of table names to fetch data from.

    Returns:
        A dictionary where the keys are table names and values are DataFrames.
    """
    dataframes = {}
    for table in table_names:
        dataframes[table] = pd.read_sql(f"SELECT * FROM {table}", connection)
        log.info("Reading %s.", table_names)

    return dataframes


def rename_columns(
    track_df: pd.DataFrame,
    album_df: pd.DataFrame,
    genre_df: pd.DataFrame,
    invoiceline_df: pd.DataFrame,
) -> tuple:
    """
    Rename columns in staging DataFrames to avoid duplication during merging.

    Args:
        track_df (pd.DataFrame): DataFrame with track information.
        album_df (pd.DataFrame): DataFrame with album information.
        genre_df (pd.DataFrame): DataFrame with genre information.
        invoiceline_df (pd.DataFrame): DataFrame with invoice information.

    Returns:
        A tuple where DataFrames with changed column names.
    """
    track_df = track_df.rename(columns={"Name": "Track_name"})
    album_df = album_df.rename(columns={"Title": "Album_title"})
    genre_df = genre_df.rename(columns={"Name": "Genre_name"})

    return track_df, album_df, genre_df, invoiceline_df


def merge_dfs(
    track_df: pd.DataFrame,
    album_df: pd.DataFrame,
    genre_df: pd.DataFrame,
    invoiceline_df: pd.DataFrame,
) -> tuple:
    """
    Merge DataFrames for further analysis.

    Args:
        track_df (pd.DataFrame): Clean DataFrame with track information.
        album_df (pd.DataFrame): Clean DataFrame with album information.
        genre_df (pd.DataFrame): Clean DataFrame with genre information.
        invoiceline_df (pd.DataFrame): DataFrame with invoice information.

    Returns:
        tuple: New merged DataFrames.
    """
    # Merging dataframes that show sales data
    join_invoice_df = invoiceline_df.merge(
        track_df, how="left", on=["TrackId", "UnitPrice"]
    )
    join_genre_df = join_invoice_df.merge(genre_df, how="left", on="GenreId")
    join_album_df = join_genre_df.merge(album_df, how="left", on="AlbumId")

    # Merging dataframes that show quantity data
    join_track_df = track_df.merge(genre_df, how="left", on="GenreId")
    join_track_plus_sales_df = join_track_df.merge(
        invoiceline_df, how="left", on="TrackId"
    )

    return join_album_df, join_genre_df, join_track_plus_sales_df


def aggregate_dfs(
    join_album_df: pd.DataFrame,
    join_genre_df: pd.DataFrame,
    join_track_plus_sales_df: pd.DataFrame,
) -> tuple:
    """
    Aggregated calculations for new data granularity.

    Args:
        join_album_df (pd.DataFrame): Merged DataFrame with whole information about albums.
        join_genre_df (pd.DataFrame): Merged DataFrame with whole information about genres.
        join_track_plus_sales_df (pd.DataFrame): Merged DataFrame with track sales information.

    Returns:
        tuple: Aggregated DataFrames.
    """
    # Groupby best genres
    genre_count = {"TrackId": ["count"], "InvoiceId": ["count"], "UnitPrice": ["sum"]}
    genre_df_agg = join_genre_df.groupby(["Genre_name"]).agg(genre_count).reset_index()
    genre_df_agg.columns = ["Genre_name", "TrackId", "InvoiceId", "UnitPrice"]

    # Groupby best albums
    album_count = {"InvoiceId": ["count"], "UnitPrice": ["sum"]}
    album_df_agg = (
        join_album_df.groupby(["Album_title", "Genre_name"])
        .agg(album_count)
        .reset_index()
    )

    album_df_agg.columns = ["Album_title", "Genre_name", "InvoiceId", "UnitPrice"]

    # Groupby count of sales in each genre
    track_inv_df_agg = (
        join_track_plus_sales_df.groupby(["Genre_name", "Track_name"])
        .agg(Bin=("InvoiceId", "count"))
        .reset_index()
    )

    bin_count_df = (
        track_inv_df_agg.groupby(["Genre_name", "Bin"])
        .agg(Bin_count=("Bin", "count"))
        .reset_index()
    )

    return album_df_agg, genre_df_agg, bin_count_df


def get_top_records(album_df_agg: pd.DataFrame, genre_df_agg: pd.DataFrame) -> tuple:
    """
    Sort and get data for top records.

    Args:
        album_df_add (pd.DataFrame): DataFrame with whole information about albums.
        genre_df_agg (pd.DataFrame): DataFrame with whole information about genres.

    Returns:
        tuple: Top most popular albums ans genres.
    """
    # Top 10 albums
    album_sorted = album_df_agg.sort_values(by="InvoiceId", ascending=False)
    top_10_albums = album_sorted.head(10)

    # Top 5 genres
    genres_sorted = genre_df_agg.sort_values(by="InvoiceId", ascending=False)
    top_5_genres = genres_sorted.head(5)

    return top_10_albums, top_5_genres


def transform_df(
    track_df: pd.DataFrame,
    album_df: pd.DataFrame,
    genre_df: pd.DataFrame,
    invoiceline_df: pd.DataFrame,
) -> tuple:
    """
    Stage raw data for plotting.

    Args:
        raw_df (pd.DataFrame): Raw Music store inventory data.

    Returns:
        pd.DataFrame: Staging data.
    """
    track_df, album_df, genre_df, invoiceline_df = rename_columns(
        track_df, album_df, genre_df, invoiceline_df
    )

    log.info("Columns have been renamed.")

    join_album_df, join_genre_df, join_track_plus_sales_df = merge_dfs(
        track_df, album_df, genre_df, invoiceline_df
    )

    log.info("Merging dataframes ended.")

    album_df_agg, genre_df_agg, bin_count_df = aggregate_dfs(
        join_album_df, join_genre_df, join_track_plus_sales_df
    )

    log.info("Aggregating dataframes ended.")

    top_10_albums, top_5_genres = get_top_records(album_df_agg, genre_df_agg)

    log.info("Top records dataframes created.")

    return top_10_albums, top_5_genres, bin_count_df


def create_plot(  # pylint: disable=too-many-arguments
    plot_type: Literal["bar", "scatter"],
    data,
    x_col,
    y_col,
    hue_col,
    xlabel,
    ylabel,
    palette="bright",
    rotation=80,
    plot_name="",
):
    """
    Plots a bar or scatter chart for different data.

    Args:
        plot_type (str): Name of Seaborn plot to create. Pick one method from supported by function.
        data: DataFrame containing the data to plot.
        x_col: Column name for the x-axis.
        y_col: Column name for the y-axis.
        hue_col: Column name for the hue (optional).
        xlabel: Label for the x-axis.
        ylabel: Label for the y-axis.
        palette: Color palette for the barplot (default is "bright").
        rotation: Rotation angle for x-axis labels (default is 80).
        plot_name: Plot name that you want to save. !!!Be sure to add .png in the end.!!!
    """
    log.info("Creating %s.", plot_name)

    plt.figure()

    # Plot type handler
    if plot_type == "bar":
        plot = sns.barplot(data=data, x=x_col, y=y_col, hue=hue_col, palette=palette)
    else:
        plot = sns.scatterplot(
            data=data, x=x_col, y=y_col, hue=hue_col, palette=palette
        )

    plot.set_xlabel(xlabel, fontsize=10)
    plot.set_ylabel(ylabel, fontsize=10)
    if hue_col:
        plot.legend(fontsize=8)
    plt.setp(plot.get_xticklabels(), rotation=rotation, fontsize=6)
    plt.tight_layout()
    full_path = PLOTS_PATH + plot_name

    # Save the plot if save_path is specified
    if plot_name:
        plt.savefig(full_path, dpi=300, format="png")
    plt.show()


def upload_plots(
    top_10_albums: pd.DataFrame, top_5_genres: pd.DataFrame, bin_count_df: pd.DataFrame
):
    """
    Upload plots to the folder /plots.

    Args:
        top_5_albums (pd.DataFrame): DataFrame used to plot 'top10 albums'.
        top_5_genres (pd.DataFrame): DataFrame used to plot 'top5 genres'.
        bin_count_df (pd.DataFrame): DataFrame used to plot 'sales count by genre'.
    """
    # Create bar plot for top-5 albums
    create_plot(
        "bar",
        data=top_10_albums,
        x_col="Album_title",
        y_col="InvoiceId",
        hue_col="Genre_name",
        xlabel="Album",
        ylabel="Number of sales",
        palette="bright",
        rotation=80,
        plot_name="top10_albums.png",
    )

    # Create bar plot for top-5 genres
    create_plot(
        "bar",
        data=top_5_genres,
        x_col="Genre_name",
        y_col="InvoiceId",
        hue_col=None,
        xlabel="Genre",
        ylabel="Number of sales",
        palette="bright",
        rotation=80,
        plot_name="top5_genres.png",
    )

    # Create scatter plot for count of sales in each genre
    create_plot(
        "scatter",
        data=bin_count_df,
        x_col="Genre_name",
        y_col="Bin_count",
        hue_col="Bin",
        xlabel="Genre",
        ylabel="Number of sales",
        palette="bright",
        rotation=80,
        plot_name="count_of_sales_in_each_genre.png",
    )

    log.info("Plots uploaded.")


def main():
    """Main process"""

    log.info("Starting the data processing pipeline...")

    # SQLite Connection init
    conn = sq.connect(CONN_URL)

    log.info("Successfull connection with database.")

    # Read tables from database
    dataframes = read_data_from_db(conn, TABLE_NAMES)
    track_df = dataframes["Track"]
    album_df = dataframes["Album"]
    genre_df = dataframes["Genre"]
    invoiceline_df = dataframes["InvoiceLine"]
    log.info("All tables have been read.")

    # Transform data to the shape and format
    top_10_albums, top_5_genres, bin_count_df = transform_df(
        track_df, album_df, genre_df, invoiceline_df
    )

    # Load data to the object storage
    upload_plots(top_10_albums, top_5_genres, bin_count_df)

    log.info("DONE!")


if __name__ == "__main__":
    main()
