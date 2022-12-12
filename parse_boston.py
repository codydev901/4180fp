from typing import List
import pandas as pd
import numpy as np
import datetime

"""
Doc Doc Doc
"""

BOSTON_FILES = ["boston_crime-incident-reports-2018.csv",
                "boston_crime-incident-reports-2019.csv",
                "boston_crime-incident-reports-2020.csv",
                "boston_crime-incident-reports-2021.csv",
                "boston_crime-incident-reports-2022.csv"]


def get_boston_crime_df(df: pd.DataFrame, keep_columns: List[str]):

    # Filter to only columns of interest
    sub_df = df[keep_columns]

    # Check Unique on Primary Type
    # print(sub_df["OFFENSE_CODE_GROUP"].unique())

    # Check Unique on Description
    # print(sub_df["OFFENSE_DESCRIPTION"].unique())

    # ^ So Primary Type looks to be what we are most interested in

    # Clean up column names a little
    sub_df = sub_df.rename(columns={"OCCURRED_ON_DATE": "date", "OFFENSE_CODE_GROUP": "crime_type",
                                    "INCIDENT_NUMBER": "crime_id"})

    # Remove columns we don't care about (keep crime_id for sanity checking later)
    sub_df = sub_df[["date", "crime_type", "crime_id"]]

    # print("PRE DATE")
    # print(sub_df.head())
    # print(sub_df.tail())

    # Remove hour/minute/second from the date strings
    sub_df["date"] = sub_df["date"].apply(lambda x: x.split(" ")[0])

    # Convert to datetime object
    sub_df["date"] = sub_df["date"].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d"))

    # Remove dates before 2018
    sub_df = sub_df[sub_df["date"] >= datetime.datetime.strptime("01/01/2018", "%m/%d/%Y")]

    # print("POST DATE")
    # print(sub_df.head())
    # print(sub_df.tail())

    # GroupBy date & crime_type, count crime_type at each date
    date_crime_groups = sub_df.groupby(["date", "crime_type"])["crime_type"].count()

    # Unique Crime Types
    crime_types = sub_df["crime_type"].unique().tolist()

    # Construct parsed_df from the groups
    parsed_df = [["date"] + crime_types]

    # Probably a cleaner way to do this.. but basically does a transpose with just the crime_types and sets to
    # 0 if none there etc.
    date = None
    date_dict = {crime_type: 0 for crime_type in crime_types}
    for i, count in date_crime_groups.iteritems():
        if not date:
            date = i[0]
        if date != i[0]:
            crime_count_row = [date_dict[k] for k in crime_types]
            parsed_df.append([date] + crime_count_row)
            date = i[0]
            date_dict = {crime_type: 0 for crime_type in crime_types}

        date_dict[i[1]] = count

    # Convert to dataframe
    parsed_df = pd.DataFrame(data=parsed_df[1:], columns=parsed_df[0])

    # Add in city
    parsed_df["city"] = ["Boston"] * len(parsed_df)

    # print("Parsed")
    # print(parsed_df.head())
    # print(parsed_df.tail())

    return parsed_df


def handle_boston_offense_code_groups():
    """
    The 2018 data has "OFFENSE_CODE_GROUP" populated, but the others years don't. Will first attempt to build a map
    with the 2018 data
    """

    df = pd.read_csv("raw_data/boston_crime-incident-reports-2018.csv")

    offense_code_group_lu = {}

    for i, row in df.iterrows():
        offense_code = row["OFFENSE_CODE"]
        offense_code_group = row["OFFENSE_CODE_GROUP"]

        if offense_code not in offense_code_group_lu:
            offense_code_group_lu[offense_code] = offense_code_group
            continue

        if offense_code_group_lu[offense_code] != offense_code_group:
            print("Mismatch: ", offense_code_group_lu[offense_code], offense_code_group, offense_code)

    return offense_code_group_lu


def find_missing_offense_codes(full_df: pd.DataFrame, offense_code_group_lu: dict):

    need_map = []
    # Check
    for i, row in full_df.iterrows():
        if row["OFFENSE_CODE"] not in offense_code_group_lu:
            need_map.append(row["OFFENSE_CODE"])

    print(len(need_map))
    print(len(full_df))

    need_map = list(set(need_map))

    print(need_map)

    # So need to map these codes
    # 12190 Affected Records
    # 389894 Total Records
    # [3200, 641, 2950, 1800, 650, 400, 530, 531, 3350, 3100, 99999, 800, 2600, 300, 1200, 3126, 3000, 700, 3005, 2500,
    # 1100, 600, 1500, 990, 2400, 736, 3300, 100, 1000, 2671, 2672, 500, 1400, 121, 122]


def main():

    # Since Boston data is separated by year in raw form, read and concat
    df = pd.concat([pd.read_csv(f"raw_data/{v}") for v in BOSTON_FILES])

    # Special Case to map offense codes to offense_code_group
    offense_code_group_lu = handle_boston_offense_code_groups()

    # Set Offense Code Group Properly
    df["OFFENSE_CODE_GROUP"] = df["OFFENSE_CODE"].apply(lambda x: offense_code_group_lu.get(x, np.nan))

    # Exploratory
    # print(df.head())
    # print(df.columns.tolist())
    # print(df.iloc[0, :].tolist())
    # print(df["OFFENSE_CODE_GROUP"].unique())

    # So looks like these are the things we will want to keep
    columns_of_interest = ["INCIDENT_NUMBER", "OCCURRED_ON_DATE", "OFFENSE_CODE_GROUP", "OFFENSE_DESCRIPTION"]

    # Parse
    parsed_df = get_boston_crime_df(df, columns_of_interest)

    # Write
    parsed_df.to_csv("parsed_data/boston_crime.csv", index=False)


if __name__ == "__main__":

    main()


