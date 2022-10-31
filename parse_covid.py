import pandas as pd
import datetime

"""
From Proposal,

COVID Case Data
Inspiration: For this I will use the dataset we have used this semester from class, the JHU CSSE COVID-119 Dataset.
Source: John Hopkins University Center for Systems Science and Engineering. Daily updates.
https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series
Format: .csv. Will filter to counties/states of interest (will be sure to note this since data on county level not city). Some extra work to calculate daily case count.
Available Variables: ['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key', ‘<Dates>’..s]
Organization: Tabular, comma delimited.

This script parses that .csv.
"""

CHICAGO_COMBINED_KEY = "Cook, Illinois, US"
BOSTON_COMBINED_KEY = "Suffolk, Massachusetts, US"
MEMPHIS_COMBINED_KEY = "Shelby, Tennessee, US"

CITY_LU = {CHICAGO_COMBINED_KEY: "Chicago",
           BOSTON_COMBINED_KEY: "Boston",
           MEMPHIS_COMBINED_KEY: "Memphis"}


def get_daily_case_df(df: pd.DataFrame, combined_key: str):
    """
    Using the combined_key (which represents a US County), return a new dataframe
    containing only cases from that county, where columns are

    city, date, daily_cases, total_cases
    """

    # Filter to county of interest
    sub_df = df[df["Combined_Key"] == combined_key]

    # Get list of current headers
    headers = df.columns.tolist()

    # Remove non-dates from header list
    date_headers = [v for v in headers if "/" in v]

    # Keep only our date columns
    sub_df = sub_df[date_headers]

    # Transpose
    sub_df = sub_df.T

    # Rename the default column header (total_cases at each day)
    sub_df = sub_df.rename(columns={sub_df.columns[0]: "total_cases"})

    # Make dates their own column (they were transposed to row names)
    sub_df["date"] = date_headers

    # Convert to datetime object
    sub_df["date"] = sub_df["date"].apply(lambda x: datetime.datetime.strptime(x, "%m/%d/%y"))

    # Change row names back to indices
    sub_df.index = list(range(len(date_headers)))

    # Calculate daily cases
    sub_df["daily_cases"] = sub_df["total_cases"].diff()

    # Fill NA (first one)
    sub_df["daily_cases"] = sub_df["daily_cases"].fillna(0.0)

    # Add in City
    sub_df["city"] = [CITY_LU[combined_key]]*len(date_headers)

    # Change case datatypes
    sub_df["total_cases"] = sub_df["total_cases"].astype('int32')
    sub_df["daily_cases"] = sub_df["daily_cases"].astype('int32')

    # Reorder columns (just to clean up)
    sub_df = sub_df[["city", "date", "daily_cases", "total_cases"]]

    return sub_df


def main():

    # Read Source DF
    df = pd.read_csv("raw_data/time_series_covid19_confirmed_US.csv")

    # Calc daily cases for each
    boston_cases = get_daily_case_df(df, BOSTON_COMBINED_KEY)
    chicago_cases = get_daily_case_df(df, CHICAGO_COMBINED_KEY)
    memphis_cases = get_daily_case_df(df, MEMPHIS_COMBINED_KEY)

    # Concat and Write
    concat_df = pd.concat([boston_cases, chicago_cases, memphis_cases])

    concat_df.to_csv("parsed_data/daily_covid_cases.csv", index=False)


if __name__ == "__main__":

    main()




