# README

## Overview

This folder contains the code used to prepare and analyze publicly available MTA NYCT data for a skills exercise. The analysis focuses on B Line performance trends during 2024–2025.

Raw data files are not included; all inputs are sourced from the New York Open Data Portal and can be downloaded as CSV files manually. It is also possible to call the Socrata API with a library such as `sodapy`. However, the site severely limits API query size, so this would require repeated API calls and stitching together partial datasets (doable, but potentially slow).
- Subway end-to-end running times [(link)](https://data.ny.gov/Transportation/MTA-Subway-End-to-End-Running-Times-Beginning-2019/sp9g-mzjh/about_data)
- Subway schedules in 2024 [(link)](https://data.ny.gov/Transportation/MTA-Subway-Schedules-2024/ebrw-j62c/about_data)
- Subway schedules in 2025 [(link)](https://data.ny.gov/Transportation/MTA-Subway-Schedules-2025/q9nv-uegs/about_data)
- Subway trains delayed [(link)](https://data.ny.gov/Transportation/MTA-Subway-Trains-Delayed-Beginning-2020/9zbp-wz3y/about_data)

## Files

`data_prep.py`:
Loads raw CSV files, performs basic type checking and filtering, and stores the cleaned data in a local SQLite database for analysis.

`analysis.ipynb`:
Performs all analysis and generates figures used in the presentation, including on-time performance, service delivered, runtime lag, and runtime variability.

## Execution order

1. Download local copies of the datasets and store them in the `data/` folder with the proper names (if this folder does not exist, create it):
    - `delays_all-trains.csv` for the "Subway Trains Delayed" dataset (pre-filtered on the time period 2024-2025)
    - `running_times_all-trains.csv` for the "Subway End-to-End Running Times" dataset (pre-filtered on the time period 2024-2025)
    - `schedule_2024_b-line.csv` for the "Subway schedules in 2024" dataset (pre-filtered to just B line trains to save disk space)
    - `schedule_2025_b-line.csv` for the "Subway schedules in 2025" dataset (pre-filtered to just B line trains to save disk space)
2. Run `data_prep.py` to create the SQLite database from the raw CSV inputs.
3. Open and run `analysis.ipynb` to reproduce the analysis and figures.


## Methodology
### Analytical approach and key assumptions
The analysis considered a few related performance metrics, obtained through appropriate columns in the “Trains Delayed” and “End-to-End Running Times” datasets:
- On-time performance, defined as 1 – (# delays)/(# scheduled trains), expressed as a percentage
- Service delivered, defined as (# actual trains)/(# scheduled trains), expressed as a percentage
- Average lag time, defined as (avg. actual runtime) – (avg. scheduled runtime) in minutes
- Runtime variability, defined as (75th percentile runtime) – (25th percentile runtime) in minutes

Trends in these metrics were compared against service pattern trends derived from the subway schedule. The four most common service patterns were assumed to represent operations as a whole, outside of a specific time period labeled “Modified service” in the presentation.

Other key assumptions:
- Hourly analyses of train frequencies at key stations (145 St and Bedford Park Blvd) are assumed to be representative proxies for changes in the main service pattern frequencies 
- On-time performance is assumed to be a reasonable stand-in for overall subway performance
- Attribution of delays to reporting categories is assumed to be stable over the analysis period

### Limitations and areas for future work
The scope of this analysis has a few key limitations:
- Uncertainty evaluation of performance improvement claims was not performed
- “Representative examples” of trends in lag time and runtime variability are identified through visual inspection, without formal statistical analysis
- The available data is not able to establish causal links. Analysis is limited to establishing correlation and mathematical relation (e.g., delay counts affecting on-time performance)

Potential future directions include:
- Station-level analysis of delays and related metrics like excess wait time could identify specific locations responsible for high runtime variability
