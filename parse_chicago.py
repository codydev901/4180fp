from typing import List
import pandas as pd
import datetime

"""
Doc Doc Doc
"""


def get_chicago_crime_df(df: pd.DataFrame, keep_columns: List[str]):

    # Filter to only columns of interest
    sub_df = df[keep_columns]

    # Check Unique on Primary Type
    # print(sub_df["Primary Type"].unique())

    # Check Unique on Description
    # print(sub_df["Description"].unique())

    # ^ So Primary Type looks to be what we are most interested in

    # Clean up column names a little
    sub_df = sub_df.rename(columns={"Date": "date", "Primary Type": "crime_type", "ID": "crime_id"})

    # Remove columns we don't care about (keep crime_id for sanity checking later)
    sub_df = sub_df[["date", "crime_type", "crime_id"]]

    # Remove hour/minute/second from the date strings
    sub_df["date"] = sub_df["date"].apply(lambda x: x.split(" ")[0])

    # Convert to datetime object
    sub_df["date"] = sub_df["date"].apply(lambda x: datetime.datetime.strptime(x, "%m/%d/%Y"))

    # Remove dates before 2018
    sub_df = sub_df[sub_df["date"] >= datetime.datetime.strptime("01/01/2018", "%m/%d/%Y")]

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
    parsed_df["city"] = ["Chicago"] * len(parsed_df)

    print(parsed_df.head())
    print(parsed_df.tail())

    return parsed_df


def main():

    # Read Source DF
    df = pd.read_csv("raw_data/chicago_Crimes_-_2001_to_Present.csv")

    # Exploratory
    print(df.head())
    print(df.columns.tolist())
    print(df.iloc[0, :].tolist())

    # So looks like these are the things we will want to keep
    columns_of_interest = ["ID", "Date", "Primary Type", "Description", "Domestic"]

    # Parse
    parsed_df = get_chicago_crime_df(df, columns_of_interest)

    # Write
    parsed_df.to_csv("parsed_data/chicago_crime.csv", index=False)


if __name__ == "__main__":

    main()
