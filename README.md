# README -- PAU Analyst Skills Exercise

## Overview

This folder contains the code used to prepare and analyze publicly available MTA NYCT data for a skills exercise. The analysis focuses on B Line performance trends during 2024–2025.

Raw data files are not included; all inputs are sourced from the New York Open Data Portal as specified in the assignment.

## Files

`data_prep.py`:
Loads raw CSV files, performs basic type checking and filtering, and stores the cleaned data in a local SQLite database for analysis.

`analysis.ipynb`:
Performs all analysis and generates figures used in the presentation, including on-time performance, service delivered, runtime lag, and runtime variability.

## Execution order

1. Download local copies of the datasets and store them in the `data/` folder.
2. Run `data_prep.py` to create the SQLite database from the raw CSV inputs.
3. Open and run `analysis.ipynb` to reproduce the analysis and figures.