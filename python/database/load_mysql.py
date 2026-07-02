import pandas as pd
import mysql.connector
from pathlib import Path

# ------------------------------------
# Database Configuration
# ------------------------------------

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "MalikHusainLalji@5253  ",
    "database": "capital_markets"
}

# ------------------------------------
# Processed Data Folder
# ------------------------------------

DATA_PATH = Path("data/processed")

FILES = {
    "clients.csv": "clients",
    "companies.csv": "companies",
    "stock_prices.csv": "stock_prices",
    "trades.csv": "trades",
    "market_indices.csv": "market_indices"
}


def get_table_columns(cursor, table_name):
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    return [row[0] for row in cursor.fetchall()]


def load_table(connection, cursor, file_name, table_name):

    print("=" * 60)
    print(f"Loading {table_name}")
    print("=" * 60)

    df = pd.read_csv(DATA_PATH / file_name)

    table_columns = get_table_columns(cursor, table_name)

    df = df[[c for c in df.columns if c in table_columns]]

    df = df.where(pd.notnull(df), None)

    placeholders = ",".join(["%s"] * len(df.columns))

    columns = ",".join(df.columns)

    sql = f"""
        INSERT INTO {table_name}
        ({columns})
        VALUES ({placeholders})
    """

    rows = [tuple(row) for row in df.values]

    try:

        cursor.executemany(sql, rows)

        connection.commit()

        print(f"SUCCESS : {len(rows)} rows inserted.")

    except Exception as e:

        connection.rollback()

        print("FAILED")

        print(e)


def main():

    connection = mysql.connector.connect(**DB_CONFIG)

    cursor = connection.cursor()

    for file_name, table_name in FILES.items():

        load_table(
            connection,
            cursor,
            file_name,
            table_name
        )

    cursor.close()

    connection.close()

    print("\nETL Completed Successfully")


if __name__ == "__main__":

    main()