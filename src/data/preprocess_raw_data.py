"""Clean initial raw data"""
import logging

import click
import numpy as np
import pandas as pd
from helper import auto_opt_pd_dtypes


def prepare_rating_data(ratings_input_path: str) -> pd.DataFrame:
    """
    Prepare raw BX-Book-Ratings.csv for the further analysis
    """
    ratings_df = pd.read_csv(ratings_input_path, sep=";", encoding_errors="replace")

    ratings_df = ratings_df.rename(
        columns={"User-ID": "user_id", "ISBN": "isbn", "Book-Rating": "rating"}
    )
    ratings_df = auto_opt_pd_dtypes(ratings_df)
    return ratings_df


def prepare_book_data(books_input_path: str) -> pd.DataFrame:
    """
    Prepare raw BX-Books.csv for the further analysis
    """
    books_df = pd.read_csv(
        books_input_path, sep=";", encoding_errors="replace", on_bad_lines="skip", low_memory=False
    )
    books_df = books_df.rename(
        columns={
            "ISBN": "isbn",
            "Book-Title": "title",
            "Book-Author": "author",
            "Year-Of-Publication": "year",
            "Publisher": "publisher",
            "Image-URL-L": "img_url",
        }
    )

    books_df = books_df.drop(columns=["Image-URL-S", "Image-URL-M"])

    # Fix year column
    # Note: for some reason direct astype(int) failed to convert numeric strings
    # We will select and update them directly
    numeric_strings_filter = books_df["year"].str.isnumeric() == True
    books_df.loc[numeric_strings_filter, "year"] = books_df.loc[
        numeric_strings_filter, "year"
    ].astype(int)
    # Replace lefted completely damaged string by NaNs
    books_df["year"] = pd.to_numeric(
        books_df["year"], errors="coerce", downcast="integer"
    )
    # Fix publishing time range
    abnormal_years = ~((0 < books_df["year"]) & (books_df["year"] <= 2004))
    books_df.loc[abnormal_years, "year"] = np.nan

    books_df = books_df.dropna()
    books_df = books_df.reset_index(drop=True)
    books_df = auto_opt_pd_dtypes(books_df)
    return books_df


def prepare_user_data(users_input_path: str) -> pd.DataFrame:
    """
    Prepare raw BX-Users.csv for the further analysis
    """
    users_df = pd.read_csv(users_input_path, sep=";", encoding_errors="replace")

    users_df = users_df.rename(
        columns={
            "User-ID": "user_id",
            "ISBN": "isbn",
            "Location": "location",
            "Age": "age",
        }
    )
    # Fix age column
    abnormal_ages = (users_df["age"] <= 0) | (users_df["age"] > 100)
    users_df.loc[abnormal_ages, "age"] = np.nan

    # Extract geo data from raw location column
    users_df["city"] = users_df["location"].str.split(",").str[0]
    users_df["country"] = users_df["location"].str.split(",").str[-1]
    users_df["city"] = users_df["city"].str.lower().str.strip()
    users_df["country"] = users_df["country"].str.lower().str.strip()
    re_remove_trash = r"[^a-zA-Z\s]"
    users_df["city"] = users_df["city"].str.replace(re_remove_trash, "", regex=True)
    users_df["country"] = users_df["country"].str.replace(
        re_remove_trash, "", regex=True
    )
    users_df.loc[users_df["city"] == "", "city"] = np.nan
    users_df.loc[users_df["country"] == "", "country"] = np.nan

    users_df = auto_opt_pd_dtypes(users_df)
    return users_df


@click.command()
@click.argument("ratings_input_path", type=click.Path())
@click.argument("books_input_path", type=click.Path())
@click.argument("users_input_path", type=click.Path())
@click.argument("ratings_output_path", type=click.Path())
@click.argument("books_output_path", type=click.Path())
@click.argument("users_output_path", type=click.Path())
def preprocess(
    ratings_input_path: str,
    books_input_path: str,
    users_input_path: str,
    ratings_output_path: str,
    books_output_path: str,
    users_output_path: str,
) -> None:
    """
    Add docsting here
    """
    logging.basicConfig(level=logging.INFO)
    logging.info("Preprocess raw data")

    ratings_df = prepare_rating_data(ratings_input_path)
    books_df = prepare_book_data(books_input_path)
    users_df = prepare_user_data(users_input_path)

    ratings_df.to_csv(ratings_output_path, index=False)
    books_df.to_csv(books_output_path, index=False)
    users_df.to_csv(users_output_path, index=False)


if __name__ == "__main__":
    preprocess()
