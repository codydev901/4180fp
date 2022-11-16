import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from typing import List
from plotly.subplots import make_subplots
import plotly.graph_objs as go

"""
Doc Doc Doc
"""

memphis_crime_types = ['Robbery', 'Assault', 'Drugs', 'Theft',
                       'Weapons Offense', 'Breaking & Entering',
                       'Property Crime', 'Theft of Vehicle', 'Theft from Vehicle',
                       'Liquor', 'Arson', 'Disorder', 'Traffic', 'Vehicle Recovery',
                       'Family Offense', 'Kidnapping', 'Homicide']

chicago_crime_types = ['THEFT', 'DECEPTIVE PRACTICE', 'OTHER OFFENSE', 'MOTOR VEHICLE THEFT', 'CRIMINAL DAMAGE', 'ASSAULT', 'BATTERY', 'NARCOTICS', 'WEAPONS VIOLATION', 'OFFENSE INVOLVING CHILDREN', 'ROBBERY', 'CRIMINAL TRESPASS', 'LIQUOR LAW VIOLATION', 'BURGLARY', 'INTERFERENCE WITH PUBLIC OFFICER', 'CRIM SEXUAL ASSAULT', 'ARSON', 'CRIMINAL SEXUAL ASSAULT', 'PROSTITUTION', 'PUBLIC PEACE VIOLATION', 'SEX OFFENSE', 'STALKING', 'KIDNAPPING', 'INTIMIDATION', 'CONCEALED CARRY LICENSE VIOLATION', 'GAMBLING', 'OBSCENITY', 'HOMICIDE', 'NON-CRIMINAL', 'HUMAN TRAFFICKING', 'PUBLIC INDECENCY', 'NON-CRIMINAL (SUBJECT SPECIFIED)', 'OTHER NARCOTIC VIOLATION', 'RITUALISM']

boston_crime_types = ['Investigate Person', 'Larceny', 'Harassment', 'Property Lost', 'Fraud', 'Auto Theft', 'Counterfeiting', 'Confidence Games', 'Commercial Burglary', 'Vandalism', 'Other', 'Missing Person Reported', 'Police Service Incidents', 'License Plate Related Incidents', 'Residential Burglary', 'Simple Assault', 'Property Found', 'Larceny From Motor Vehicle', 'Medical Assistance', 'Motor Vehicle Accident Response', 'Aggravated Assault', 'Landlord/Tenant Disputes', 'Investigate Property', 'Auto Theft Recovery', 'Missing Person Located', 'Embezzlement', 'Violations', 'Criminal Harassment', 'Disorderly Conduct', 'Warrant Arrests', 'Other Burglary', 'Restraining Order Violations', 'Recovered Stolen Property', 'Service', 'Property Related Damage', 'Robbery', 'Towed', 'Evading Fare', 'License Violation', 'Verbal Disputes', 'Fire Related Reports', 'Firearm Violations', 'Search Warrants', 'Operating Under the Influence', 'Drug Violation', 'Prisoner Related Incidents', 'Firearm Discovery', 'Ballistics', 'Liquor Violation', 'Homicide', 'Offenses Against Child / Family', 'Harbor Related Incidents', 'Arson', 'Assembly or Gathering Violations', 'Bomb Hoax', 'Aircraft', 'Phone Call Complaints', 'Prostitution', 'HUMAN TRAFFICKING', 'HOME INVASION', 'Explosives', 'Unnamed: 62']


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

    fig = px.line(combined_df, x="date", y=["daily_cases"] + memphis_crime_types, markers=True,
                  title="Relative Frequency of Selected Crime Types and COVID Cases vs. Date")
    fig.show()


def plot_compare_city_daily_cases_and_crime(case_df: pd.DataFrame, crime_df: pd.DataFrame, city_name: str,
                                            city_crime_types: List[str]):

    # Probably better way to do this
    # Crime DataFrame has more dates than covid cases.
    # So need to add empty dates to the case count for merging later (so to see crime before covid etc)
    sub_case_df = case_df[case_df["city"] == city_name]
    case_dates = sub_case_df["date"].unique().tolist()
    crime_dates = crime_df["date"].unique().tolist()
    for crime_d in crime_dates:
        if crime_d not in case_dates:
            new_row = {'city': city_name, 'date': crime_d, 'daily_cases': 0, 'total_cases': 0}
            sub_case_df = sub_case_df.append(new_row, ignore_index=True)

    # Merge
    combined_df = crime_df.merge(sub_case_df, on="date")

    print(combined_df.head())
    print(combined_df.tail())
    print("OK")
    exit()

    # Floor Date By Month/Sum Crime/Case Counts
    combined_df["date"] = pd.to_datetime(combined_df.date).dt.to_period('M').dt.to_timestamp()
    temp_agg = {k: 'sum' for k in city_crime_types}
    temp_agg["daily_cases"] = "sum"
    combined_df = combined_df.groupby(["date"], as_index=False).agg(temp_agg)

    # Min/Max Normalization
    for k in ["daily_cases"] + city_crime_types:
        k_max = combined_df[k].max()
        combined_df[k] = combined_df[k].apply(lambda x: x/k_max)


    # print(combined_df.head())

    fig = px.line(combined_df, x="date", y=["daily_cases"] + city_crime_types, markers=True,
                  title=f"Relative Frequency of Selected Crime Types and COVID Cases vs. Date: {city_name}")
    fig.show()


def covid_case_plot(covid_case_df: pd.DataFrame):

    max_map = {}
    for city in covid_case_df['city'].unique().tolist():
        max_daily_case = covid_case_df[covid_case_df["city"] == city]["daily_cases"].max()
        max_map[city] = max_daily_case

    normalized_cases = []
    for i, row in covid_case_df.iterrows():
        d_c = row["daily_cases"]
        normalized_cases.append(d_c / max_map[row['city']])
    covid_case_df["daily_cases_normalized"] = normalized_cases

    fig = px.scatter(covid_case_df, x="date", y=["daily_cases_normalized"], color="city",
                     title="Normalized Daily COVID Count vs. Date")
    fig.show()


def plot_combined_df_covid_cases(combined_df: pd.DataFrame):

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")

    fig = px.line(combined_df, x="month_year", y=["monthly_cases"], color="city", markers=True,
                  title=f"Normalized Monthly COVID Cases vs. Date")
    fig.show()


def plot_combined_df_crimes(combined_df: pd.DataFrame, display_crimes: List[str]):

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")  # handle elsewhere, none of these
    for c_t in list(crime_types):
        if c_t not in display_crimes:
            crime_types.remove(c_t)

    t_df = [["city", "month_year", "monthly_cases", "crime_type", "crime_frequency"]]

    for i, row in combined_df.iterrows():
        for crime_type in crime_types:
            t_df.append([row["city"], row["month_year"], row["monthly_cases"], crime_type, row[crime_type]])

    t_df = pd.DataFrame(data=t_df[1:], columns=t_df[0])

    fig = px.line(t_df, x="month_year", y="crime_frequency", color="city", facet_row="crime_type")
    fig.show()



    # fig = px.line(combined_df, x="month_year", y=["monthly_cases"], color="city", markers=True,
    #               title=f"Normalized Monthly COVID Cases vs. Date")
    # fig.show()



def main():

    city_name = "Boston"

    # Load in dataframes
    # covid_case_df = pd.read_csv("parsed_data/daily_covid_cases.csv")
    # memphis_crime_df = pd.read_csv("parsed_data/memphis_crime.csv")
    # chicago_crime_df = pd.read_csv("parsed_data/chicago_crime.csv")
    # boston_crime_df = pd.read_csv("parsed_data/boston_crime.csv")

    # Filter case to Memphis only
    # covid_case_df = covid_case_df[covid_case_df["city"] == city_name]

    # print(covid_case_df.head())
    # print(memphis_crime_df.head())

    # Plot/Compare Crime
    # print("Plot Compare Crime")
    # plot_compare_memphis_daily_cases_and_crime(covid_case_df, memphis_crime_df)
    # plot_compare_city_daily_cases_and_crime(covid_case_df, boston_crime_df, city_name, boston_crime_types)
    # covid_case_plot(covid_case_df)

    combined_df = pd.read_csv("parsed_data/combined_cases_crime_equivalent_monthly_normalized.csv")
    # print(combined_df.head())

    plot_combined_df_covid_cases(combined_df=combined_df)

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")

    plot_combined_df_crimes(combined_df, display_crimes=crime_types[12:16])


if __name__ == "__main__":

    main()
