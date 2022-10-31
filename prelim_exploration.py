import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

"""
Doc Doc Doc
"""

memphis_crime_types = ['Robbery', 'Assault', 'Drugs', 'Theft',
                       'Weapons Offense', 'Breaking & Entering',
                       'Property Crime', 'Theft of Vehicle', 'Theft from Vehicle',
                       'Liquor', 'Arson', 'Disorder', 'Traffic', 'Vehicle Recovery',
                       'Family Offense', 'Kidnapping', 'Homicide']


def plot_compare_daily_cases_by_city(df: pd.DataFrame):

    pass


def plot_compare_memphis_daily_cases_and_crime(case_df: pd.DataFrame, crime_df: pd.DataFrame):

    # Probably better way to do this
    # Crime DataFrame has more dates than covid cases.
    # So need to add empty dates to the case count for merging later (so to see crime before covid etc)
    sub_case_df = case_df[case_df["city"] == "Memphis"]
    case_dates = sub_case_df["date"].unique().tolist()
    crime_dates = crime_df["date"].unique().tolist()
    for crime_d in crime_dates:
        if crime_d not in case_dates:
            new_row = {'city': 'Memphis', 'date': crime_d, 'daily_cases': 0, 'total_cases': 0}
            sub_case_df = sub_case_df.append(new_row, ignore_index=True)

    # Merge
    combined_df = crime_df.merge(sub_case_df, on="date")

    # Floor Date By Month/Sum Crime/Case Counts
    combined_df["date"] = pd.to_datetime(combined_df.date).dt.to_period('M').dt.to_timestamp()
    temp_agg = {k: 'sum' for k in memphis_crime_types}
    temp_agg["daily_cases"] = "sum"
    combined_df = combined_df.groupby(["date"], as_index=False).agg(temp_agg)

    # Min/Max Normalization
    for k in ["daily_cases"] + memphis_crime_types:
        k_max = combined_df[k].max()
        combined_df[k] = combined_df[k].apply(lambda x: x/k_max)

    print(combined_df.head())

    fig = px.line(combined_df, x="date", y=["daily_cases"] + memphis_crime_types, markers=True)
    fig.show()


    # combined_df.plot(kind="scatter", x="date", y="daily_cases", color="red")
    # combined_df.plot(kind="scatter", x="date", y="Homicide", color="blue")
    # plt.show()


def main():

    # Load in dataframes
    covid_case_df = pd.read_csv("parsed_data/daily_covid_cases.csv")
    memphis_crime_df = pd.read_csv("parsed_data/memphis_crime.csv")

    # Filter case to Memphis only
    covid_case_df = covid_case_df[covid_case_df["city"] == "Memphis"]

    print(covid_case_df.head())
    print(memphis_crime_df.head())

    # Plot/Compare Crime
    print("Plot Compare Crime")
    plot_compare_memphis_daily_cases_and_crime(covid_case_df, memphis_crime_df)


if __name__ == "__main__":

    main()
