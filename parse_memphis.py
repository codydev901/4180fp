from typing import List
import pandas as pd
import datetime

"""
Doc Doc Doc
"""


def get_memphis_crime_df(df: pd.DataFrame, keep_columns: List[str]):
    """
    Doc Doc Doc

    Return date, crime_type, count
    """

    # Filter to only columns of interest
    sub_df = df[keep_columns]

    # Check Unique on City
    # print(sub_df["city"].unique())  # Note: This is somewhat messy, may need to do some filtering here

    # Check Unique on Category
    # print(sub_df["Category"].unique())

    # Check Unique on Crime Type Id
    # print(sub_df["agency_crimetype_id"].unique())

    # ^ Category is more general, while crimetype_id is more specific, lets go with category for now

    # Clean up column names a little
    sub_df = sub_df.rename(columns={"offense_date": "date", "Category": "crime_type"})

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
    parsed_df["city"] = ["Memphis"]*len(parsed_df)

    return parsed_df


def main():

    # Read Source DF
    df = pd.read_csv("raw_data/Memphis_Police_Department__Public_Safety_Incidents.csv")

    # Exploratory
    # print(df.head())
    # print(df.columns.tolist())
    # print(df.iloc[0, :].tolist())
    # print(df.iloc[1, :].tolist())

    # print(len(df["agency_crimetype_id"].unique()))

    # So looks like these are the things we will want to keep
    columns_of_interest = ["offense_date", "agency_crimetype_id", "city", "state", "Category", "crime_id"]

    # Parse
    parsed_df = get_memphis_crime_df(df, columns_of_interest)

    # Write
    parsed_df.to_csv("parsed_data/memphis_crime.csv", index=False)


if __name__ == "__main__":

    main()
