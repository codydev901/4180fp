import pandas as pd
import numpy as np

from parse_covid import get_daily_case_df, BOSTON_COMBINED_KEY, CHICAGO_COMBINED_KEY, MEMPHIS_COMBINED_KEY
from parse_memphis import get_memphis_crime_df
from parse_chicago import get_chicago_crime_df
from parse_boston import get_boston_crime_df, BOSTON_FILES, handle_boston_offense_code_groups

from combine_parsed_data import make_crime_remap_lookup, normalize_and_combine_single_city
from plot_normalized_monthly import plot_combined_df_crimes
from analysis_crime_change import generate_yearly_crime_ratio_per_city_csv, plot_crime_ratio

"""
Doc Doc Doc
"""

COVID_DAILY_CASES_FILE = "daily_covid_cases.csv"
MEMPHIS_DAILY_CRIME_FILE = "memphis_crime.csv"
CHICAGO_DAILY_CRIME_FILE = "chicago_crime.csv"
BOSTON_DAILY_CRIME_FILE = "boston_crime.csv"
COMBINED_MONTHLY_NORMALIZED_FILE = "combined_cases_crime_equivalent_monthly_normalized.csv"
YEARLY_RATIO_FILE = "yearly_crime_ratio_per_city.csv"


def generate_write_covid_daily_cases():
    """
    Parses the JHU CSSE COVID-19 dataset and writes to parsed_data/daily_covid_cases.csv

    Resulting format:
    city,date,daily_cases,total_cases
    """

    print("Generate COVID Daily Cases")
    df = pd.read_csv("raw_data/time_series_covid19_confirmed_US.csv")

    # Calc daily cases for each
    boston_cases = get_daily_case_df(df, BOSTON_COMBINED_KEY)
    chicago_cases = get_daily_case_df(df, CHICAGO_COMBINED_KEY)
    memphis_cases = get_daily_case_df(df, MEMPHIS_COMBINED_KEY)

    # Concat and Write
    concat_df = pd.concat([boston_cases, chicago_cases, memphis_cases])
    concat_df.to_csv(f"parsed_data/{COVID_DAILY_CASES_FILE}", index=False)

    print("Daily Cases DF Head")
    print(concat_df.head())
    print("Daily Cases DF Tail")
    print(concat_df.tail())


def generate_write_city_daily_crime_counts():
    """
    Doc Doc Doc
    """

    # Memphis
    print("Generate Daily Memphis Crime Counts")
    df = pd.read_csv("raw_data/Memphis_Police_Department__Public_Safety_Incidents.csv")
    columns_of_interest = ["offense_date", "agency_crimetype_id", "city", "state", "Category", "crime_id"]
    parsed_df = get_memphis_crime_df(df, columns_of_interest)
    parsed_df.to_csv(f"parsed_data/{MEMPHIS_DAILY_CRIME_FILE}", index=False)

    print("Memphis Crime Daily Head")
    print(parsed_df.head())
    print("Memphis Crime Daily Tail")
    print(parsed_df.tail())

    # Chicago
    print("Generate Daily Chicago Crime Counts")
    df = pd.read_csv("raw_data/chicago_Crimes_-_2001_to_Present.csv")
    columns_of_interest = ["ID", "Date", "Primary Type", "Description", "Domestic"]
    parsed_df = get_chicago_crime_df(df, columns_of_interest)
    parsed_df.to_csv(f"parsed_data/{CHICAGO_DAILY_CRIME_FILE}", index=False)

    print("Chicago Crime Daily Head")
    print(parsed_df.head())
    print("Chicago Crime Daily Tail")
    print(parsed_df.tail())

    # Boston
    print("Generate Daily Boston Crime Counts")
    df = pd.concat([pd.read_csv(f"raw_data/{v}") for v in BOSTON_FILES])  # Note concat of multiple files
    offense_code_group_lu = handle_boston_offense_code_groups()  # Special Case to fill in missing data
    df["OFFENSE_CODE_GROUP"] = df["OFFENSE_CODE"].apply(lambda x: offense_code_group_lu.get(x, np.nan))
    columns_of_interest = ["INCIDENT_NUMBER", "OCCURRED_ON_DATE", "OFFENSE_CODE_GROUP", "OFFENSE_DESCRIPTION"]
    parsed_df = get_boston_crime_df(df, columns_of_interest)
    parsed_df.to_csv(f"parsed_data/{BOSTON_DAILY_CRIME_FILE}", index=False)

    print("Boston Crime Daily Head")
    print(parsed_df.head())
    print("Boston Crime Daily Tail")
    print(parsed_df.tail())


def generate_write_combined_equivalent_normalized_covid_and_crime_data():
    """
    Doc Doc Doc
    """

    print("Combine and Normalize COVID Cases and Crime Counts")

    # Load Crime Remapping Information
    crime_remap_lookup = make_crime_remap_lookup()

    # Load in dataframes
    covid_case_df = pd.read_csv(f"parsed_data/{COVID_DAILY_CASES_FILE}")
    memphis_crime_df = pd.read_csv(f"parsed_data/{MEMPHIS_DAILY_CRIME_FILE}")
    chicago_crime_df = pd.read_csv(f"parsed_data/{CHICAGO_DAILY_CRIME_FILE}")
    boston_crime_df = pd.read_csv(f"parsed_data/{BOSTON_DAILY_CRIME_FILE}")

    # Run for each city (so that Crime/Covid cases are normalized in context of that city)
    memphis_crime_df_norm = normalize_and_combine_single_city(covid_case_df, memphis_crime_df, city_name="Memphis",
                                                              crime_equiv_lookup=crime_remap_lookup)

    chicago_crime_df_norm = normalize_and_combine_single_city(covid_case_df, chicago_crime_df, city_name="Chicago",
                                                              crime_equiv_lookup=crime_remap_lookup)

    boston_crime_df_norm = normalize_and_combine_single_city(covid_case_df, boston_crime_df, city_name="Boston",
                                                             crime_equiv_lookup=crime_remap_lookup)

    # Combine resulting dataframes into a single one and write.
    combined_df = pd.concat([memphis_crime_df_norm, chicago_crime_df_norm, boston_crime_df_norm])
    combined_df.to_csv(f"parsed_data/{COMBINED_MONTHLY_NORMALIZED_FILE}", index=False)

    print("Combined Normalized Monthly Head")
    print(combined_df.head())
    print("Combined Normalized Monthly Tail")
    print(combined_df.tail())


def generate_save_monthly_normalized_plots(do_show: bool = False):

    combined_df = pd.read_csv(f"parsed_data/{COMBINED_MONTHLY_NORMALIZED_FILE}")

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")

    for i in range(4):
        s_i = i * 4
        e_i = s_i + 4

        plot_combined_df_crimes(combined_df, display_crimes=crime_types[s_i:e_i], crime_group=i, do_show=do_show)


def generate_save_yearly_ratio_plots(do_show: bool = False):

    combined_df = pd.read_csv(f"parsed_data/{COMBINED_MONTHLY_NORMALIZED_FILE}")
    generate_yearly_crime_ratio_per_city_csv(combined_df=combined_df)

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")

    crime_change_df = pd.read_csv(f"parsed_data/{YEARLY_RATIO_FILE}")

    for i in range(4):
        s_i = i * 4
        e_i = s_i + 4
        plot_crime_ratio(crime_change_df, keep_crimes=crime_types[s_i:e_i], crime_group=i, do_show=do_show)


def generate_overall_ratio():

    def classify_crime_ratio(ratio):

        if ratio > 1.20:
            return "more frequent"
        elif ratio < .80:
            return "less frequent"
        else:
            return "about the same"

    df = pd.read_csv("parsed_data/yearly_crime_ratio_per_city.csv")

    grouped_df = df.groupby("crime_type").agg({"crime_ratio": "mean"})

    grouped_df["desc"] = grouped_df["crime_ratio"].apply(lambda x: classify_crime_ratio(x))
    grouped_df["crime_type"] = list(grouped_df.index)

    grouped_df = grouped_df[["crime_type", "crime_ratio", "desc"]]
    grouped_df.to_csv("parsed_data/average_crime_ratio.csv", index=False)


def main():

    # Parse Daily COVID Cases
    # generate_write_covid_daily_cases()

    # Parse Daily Crime Data
    # generate_write_city_daily_crime_counts()

    # Combine and Normalize Daily Crime and COVID Cases into Monthly Representations
    # generate_write_combined_equivalent_normalized_covid_and_crime_data()

    # Generate Monthly Normalized COVID/Crime Plots
    # generate_save_monthly_normalized_plots(do_show=False)

    # Generate yearly city crime ratios
    # generate_save_yearly_ratio_plots(do_show=True)

    # Generate overall average post vs pre pandemic ratios
    generate_overall_ratio()






if __name__ == "__main__":

    main()
