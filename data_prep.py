import numpy as np
import pandas as pd
import sqlite3
import logging

import os

DATABASE_DIR = "data/subway_records.db"

def csv_to_table_by_chunks(csv_path, table_name,
                           date_cols=dict(), numeric_cols=[],
                           chunksize=100000, inspect_chunk=False,
                           replace=True):
    """Function to convert CSV data to a SQLite table by reading in chunks (to protect RAM for large CSVs)."""

    logging.info(f"Reading in: {csv_path}, and writing to table: {table_name}...")

    # Force all columns to be read as strings to start
    all_columns = pd.read_csv(csv_path, nrows=0).columns
    dtype_dict = {col: str for col in all_columns}

    # Open SQLite connection and create chunked CSV reader
    conn = sqlite3.connect(DATABASE_DIR)
    reader = pd.read_csv(csv_path, chunksize=chunksize, 
                         dtype=dtype_dict,
                         na_values=["", " ", "NULL", "NaN"])

    # Iterate over chunks
    for i, chunk in enumerate(reader):
        # Perform initial typecasting
        for col, fmt in date_cols.items():
            chunk[col] = pd.to_datetime(chunk[col], format=fmt, errors="coerce")
        for col in numeric_cols:
            chunk[col] = pd.to_numeric(chunk[col], errors="coerce")

        # Debug: don't write, just return the first chunk
        if inspect_chunk:
            conn.close()
            return(chunk)

        # Write to SQL
        mode = 'replace' if (i == 0 and replace) else 'append'
        chunk.to_sql(table_name, conn, if_exists=mode, index=False)
        logging.info(f"Chunk {i} ingested. Total rows: {i*chunksize + len(chunk)}")
    
    conn.close()

def setup_logging():
    """Log to inspect data prep"""
    log_file = "data_prep.log"

    # Set up the configuration
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),    # Writes to file
            logging.StreamHandler()           # Prints to terminal
        ]
    )
    logging.info("--- data_prep.py starting... ---")

def main():
    setup_logging()

    os.makedirs("data", exist_ok=True)
    
    logging.info("Constructing SQLite database...")

    # MTA Subway Trains Delayed: Beginning 2020
    csv_to_table_by_chunks(
        csv_path = "data/delays_all-trains.csv",
        table_name = "delays",
        date_cols = {"month": "%Y-%m-%d"},
        numeric_cols = ["day_type", "delays"]
    )

    # MTA Subway End-to-End Running Times: Beginning 2019
    csv_to_table_by_chunks(
        csv_path = "data/running_times_all-trains.csv",
        table_name = "running_times",
        date_cols = {"Month": "%m/%d/%Y"},
        numeric_cols = ["Average Actual Runtime", "25th Percentile Runtime", "50th Percentile Runtime", "75th Percentile Runtime", "Actual Trains", "Distance", "Average Speed", "Average Scheduled Runtime", "Scheduled Trains", "Number of Stops"]
    )

    # MTA Subway Schedules: 2024
    csv_to_table_by_chunks(
        csv_path = "data/schedule_2024_b-line.csv",
        table_name = "schedule",
        date_cols = {
            "Service Date": "%m/%d/%Y",
            "Arrival Time": "%m/%d/%Y %I:%M:%S %p",
            "Departure Time": "%m/%d/%Y %I:%M:%S %p",
            "Next Trip Time": "%m/%d/%Y %I:%M:%S %p"
        },
        numeric_cols = ["Stop Order", "Date Difference"]
    )

    # MTA Subway Schedules: 2025. Append to the same table as 2024.
    csv_to_table_by_chunks(
        csv_path = "data/schedule_2025_b-line.csv",
        table_name = "schedule",
        date_cols = {
            "Service Date": "%m/%d/%Y",
            "Arrival Time": "%m/%d/%Y %I:%M:%S %p",
            "Departure Time": "%m/%d/%Y %I:%M:%S %p",
            "Next Trip Time": "%m/%d/%Y %I:%M:%S %p"
        },
        numeric_cols = ["Stop Order", "Date Difference"],
        replace=False
    )

    logging.info("--- data_prep.py completed successfully! ---")

if __name__ == "__main__":
    main()