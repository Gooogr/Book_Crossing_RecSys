"""
Create if not existed or rewrite `features` table in PostreSQL DB by input csv file
"""
import logging
import os

import click
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists

load_dotenv()


@click.command()
@click.option(
    "--csv-path",
    type=click.Path(exists=True),
    default="./data/interim/books.csv",
    help="The file path to the CSV file containing the data to replace the table with.",
)
@click.option(
    "--host",
    type=str,
    default="localhost:5432",
    help="The IP address of the database.",
)
def replace_postgres_table_with_csv(csv_path, host):
    """
    Replace the contents of a PostgreSQL table with the data from a CSV file.

    Args:
    - csv_path (str): The file path to the CSV file containing the data to replace the table with.
    - host (str): The IP adress of data base.

    Returns:
    - None
    """
    logging.basicConfig(level=logging.INFO)
    df = pd.read_csv(csv_path, sep=';')

    engine = create_engine(
        f'postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}'
        f'@{host}/{os.getenv("POSTGRES_FEATURE_DB")}'
    )

    if not database_exists(engine.url):
        create_database(engine.url)
        logging.info(
            f'No database {os.getenv("POSTGRES_FEATURE_DB")} detected. Database was created.'
        )

    df.to_sql(
        name=os.getenv("POSTGRES_FEATURE_TABLE"),
        con=engine,
        if_exists="replace",
        method="multi",
    )
    logging.info("Successfully updated PostreSQL table.")


if __name__ == "__main__":
    replace_postgres_table_with_csv()