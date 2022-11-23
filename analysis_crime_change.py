import pandas as pd
import numpy as np
import plotly.express as px

from typing import List

"""
Doc Doc Doc
"""

date_range_2018 = pd.date_range(start="2018-01-01", periods=12, freq="M")
date_range_2018 = date_range_2018.to_period('M').to_timestamp().tolist()

date_range_2019 = pd.date_range(start="2019-01-01", periods=12, freq="M")
date_range_2019 = date_range_2019.to_period('M').to_timestamp()

date_range_2020 = pd.date_range(start="2020-01-01", periods=12, freq="M")
date_range_2020 = date_range_2020.to_period('M').to_timestamp()

date_range_2021 = pd.date_range(start="2021-01-01", periods=12, freq="M")
date_range_2021 = date_range_2021.to_period('M').to_timestamp()


def quick_date_parse(date_obj):

    return str(date_obj).split(" ", 1)[0]


def calc_yearly_diff(combined_df: pd.DataFrame, city: str, crime_type: str):

    # Filter DF to a particular city
    sub_df = combined_df[(combined_df["city"] == city)]

    crime_change_2020_to_2018 = []
    crime_change_2020_to_2019 = []
    crime_change_2021_to_2018 = []
    crime_change_2021_to_2019 = []

    for date_i in range(len(date_range_2018)):

        # Get the relative frequency of a crime occurring in each month/year
        crime_freq_2018 = sub_df[sub_df["month_year"] == quick_date_parse(date_range_2018[date_i])][crime_type].tolist()[0]
        crime_freq_2019 = sub_df[sub_df["month_year"] == quick_date_parse(date_range_2019[date_i])][crime_type].tolist()[0]
        crime_freq_2020 = sub_df[sub_df["month_year"] == quick_date_parse(date_range_2020[date_i])][crime_type].tolist()[0]
        crime_freq_2021 = sub_df[sub_df["month_year"] == quick_date_parse(date_range_2021[date_i])][crime_type].tolist()[0]

        try:
            crime_change_2020_to_2018.append(crime_freq_2020 / crime_freq_2018)
            crime_change_2020_to_2019.append(crime_freq_2020 / crime_freq_2019)
            crime_change_2021_to_2018.append(crime_freq_2021 / crime_freq_2018)
            crime_change_2021_to_2019.append(crime_freq_2021 / crime_freq_2019)
        except ZeroDivisionError:
            continue

    # print(city)
    # print(crime_type)
    # print(crime_change_2020_to_2018)
    # print(crime_change_2020_to_2019)
    # print(crime_change_2021_to_2018)
    # print(crime_change_2021_to_2019)

    return {"city": city, "crime_type": crime_type,
            "2020_to_2018": np.mean(crime_change_2020_to_2018),
            "2020_to_2019": np.mean(crime_change_2020_to_2019),
            "2021_to_2018": np.mean(crime_change_2021_to_2018),
            "2021_to_2019": np.mean(crime_change_2021_to_2019)}


def generate_yearly_crime_ratio_csv():

    combined_df = pd.read_csv("parsed_data/combined_cases_crime_equivalent_monthly_normalized.csv")

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")

    crime_change_data = [["city", "crime_type", "time_period", "crime_ratio"]]

    for city in combined_df["city"].unique().tolist():
        for crime_type in crime_types:
            res = calc_yearly_diff(combined_df=combined_df, city=city, crime_type=crime_type)
            crime_change_data.append([res["city"], res["crime_type"], "2020_to_2018", res["2020_to_2018"]])
            crime_change_data.append([res["city"], res["crime_type"], "2020_to_2019", res["2020_to_2019"]])
            crime_change_data.append([res["city"], res["crime_type"], "2021_to_2018", res["2021_to_2018"]])
            crime_change_data.append([res["city"], res["crime_type"], "2021_to_2019", res["2021_to_2019"]])

    crime_change_data = pd.DataFrame(data=crime_change_data[1:], columns=crime_change_data[0])
    crime_change_data.to_csv("parsed_data/yearly_crime_ratio.csv", index=False)


def plot_crime_ratio(crime_change_df: pd.DataFrame, keep_crimes: List[str]):

    sub_crime_change_df = crime_change_df[crime_change_df["crime_type"].isin(keep_crimes)]

    fig = px.scatter(sub_crime_change_df, x="time_period", y="crime_ratio", color="city", facet_col="crime_type")
    # Sub-Titles
    for anno in fig.layout.annotations:
        anno.text = anno.text.split("=", 1)[-1].strip()
    fig.show()


def main():

    combined_df = pd.read_csv("parsed_data/combined_cases_crime_equivalent_monthly_normalized.csv")
    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")

    crime_change_df = pd.read_csv("parsed_data/yearly_crime_ratio.csv")

    plot_crime_ratio(crime_change_df, keep_crimes=crime_types[:8])



if __name__ == "__main__":

    generate_yearly_crime_ratio_csv()

    main()
