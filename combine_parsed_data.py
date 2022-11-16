import pandas as pd

"""
2nd Stage of DataProcessing

Combines the Crime Data from the 3 cites + the COVID cases into a single file/dataframe so that it may be used
for final analysis.

Best judgement used to combine the crime classifications...
"""


def determine_crime_classification():
    """
    Doc Doc Doc
    """

    # Load 3 Crime Dataframes. Native Crime Types are the Headers minus date & city
    crime_memphis = pd.read_csv("parsed_data/memphis_crime.csv")
    crime_chicago = pd.read_csv("parsed_data/chicago_crime.csv")
    crime_boston = pd.read_csv("parsed_data/boston_crime.csv")

    memphis_native_types = crime_memphis.columns.tolist()
    chicago_native_types = crime_chicago.columns.tolist()
    boston_native_types = crime_boston.columns.tolist()

    memphis_native_types.remove('date')
    memphis_native_types.remove('city')
    chicago_native_types.remove('date')
    chicago_native_types.remove('city')
    boston_native_types.remove('date')
    boston_native_types.remove('city')

    # memphis_native_types = [v.lower() for v in memphis_native_types]
    # chicago_native_types = [v.lower() for v in chicago_native_types]
    # boston_native_types = [v.lower() for v in boston_native_types]

    print(memphis_native_types)
    print(chicago_native_types)
    print(boston_native_types)

    print(len(memphis_native_types))
    print(len(chicago_native_types))
    print(len(boston_native_types))

    # So Memphis Has the least number of types. We need to re-classify the others to Memphis type (or discard).
    # print("Memphis")
    # for v in memphis_native_types:
    #     print(v)
    #
    # print("Chicago")
    # for v in chicago_native_types:
    #     print(v)
    #
    # print("Boston")
    # for v in boston_native_types:
    #     print(v)

    # Made helper_data/crime_equiv.csv in GoogleSheets -- To Refine Further...


def make_remap_lu():

    crime_equiv_df = pd.read_csv("helper_data/crime_equiv - crime_equiv_v1.csv")
    remap_lu = {c: {} for c in crime_equiv_df["city"].unique().tolist()}

    for i, row in crime_equiv_df.iterrows():
        remap_lu[row["city"]][row["native_cat"]] = row["equiv_cat"]

    return remap_lu


def combine_parsed_dfs_one(remap_lu: dict):
    """
    OLD
    """

    memphis_df = pd.read_csv("parsed_data/memphis_crime.csv")
    memphis_df.columns = [v.lower() for v in memphis_df.columns]
    chicago_df = pd.read_csv("parsed_data/chicago_crime.csv")
    chicago_df.columns = [v.lower() for v in chicago_df.columns]
    boston_df = pd.read_csv("parsed_data/boston_crime.csv")
    boston_df.columns = [v.lower() for v in boston_df.columns]
    covid_df = pd.read_csv("parsed_data/daily_covid_cases.csv")

    # Get Covid Data in a way we can hash easy for below
    covid_case_lu = {c: {} for c in covid_df["city"].unique().tolist()}
    for i, row in covid_df.iterrows():
        if row["date"] not in covid_case_lu:
            covid_case_lu[row["date"]] = row["date"]
            covid_case_lu[row["date"]] = {c: None for c in covid_df["city"].unique().tolist()}
        covid_case_lu[row["date"]][row["city"]] = {"daily_cases": row["daily_cases"], "total_cases": row["total_cases"]}

    combined_df = {"city": [], "date": [], "crime_type": [], "crime_count": [], "daily_cases": [], "total_cases": []}

    # Memphis
    memphis_crime_types = memphis_df.columns.tolist()
    memphis_crime_types.remove("city")
    memphis_crime_types.remove("date")
    for i, row in memphis_df.iterrows():
        try:
            daily_cases = covid_case_lu[row["date"]][row["city"]]["daily_cases"]
        except KeyError:
            daily_cases = 0
        try:
            total_cases = covid_case_lu[row["date"]][row["city"]]["total_cases"]
        except KeyError:
            total_cases = 0

        for crime_type in memphis_crime_types:
            combined_df["city"].append(row["city"])
            combined_df["date"].append(row["date"])
            combined_df["crime_type"].append(crime_type)
            combined_df["crime_count"].append(row[crime_type])
            combined_df["daily_cases"].append(daily_cases)
            combined_df["total_cases"].append(total_cases)

    # Chicago
    chicago_crime_types = chicago_df.columns.tolist()
    chicago_crime_types.remove("city")
    chicago_crime_types.remove("date")
    for i, row in chicago_df.iterrows():
        try:
            daily_cases = covid_case_lu[row["date"]][row["city"]]["daily_cases"]
        except KeyError:
            daily_cases = 0
        try:
            total_cases = covid_case_lu[row["date"]][row["city"]]["total_cases"]
        except KeyError:
            total_cases = 0

        crime_remap_counts = {}
        for crime_type in chicago_crime_types:
            equiv_crime_type = remap_lu[row["city"]][crime_type]
            if equiv_crime_type not in crime_remap_counts:
                crime_remap_counts[equiv_crime_type] = row[crime_type]
            else:
                crime_remap_counts[equiv_crime_type] += row[crime_type]

        for k in crime_remap_counts:
            combined_df["city"].append(row["city"])
            combined_df["date"].append(row["date"])
            combined_df["crime_type"].append(k)
            combined_df["crime_count"].append(crime_remap_counts[k])
            combined_df["daily_cases"].append(daily_cases)
            combined_df["total_cases"].append(total_cases)

    # Boston
    boston_crime_types = boston_df.columns.tolist()
    boston_crime_types.remove("city")
    boston_crime_types.remove("date")
    for i, row in boston_df.iterrows():
        try:
            daily_cases = covid_case_lu[row["date"]][row["city"]]["daily_cases"]
        except KeyError:
            daily_cases = 0
        try:
            total_cases = covid_case_lu[row["date"]][row["city"]]["total_cases"]
        except KeyError:
            total_cases = 0

        crime_remap_counts = {}
        for crime_type in boston_crime_types:
            equiv_crime_type = remap_lu[row["city"]][crime_type]
            if equiv_crime_type not in crime_remap_counts:
                crime_remap_counts[equiv_crime_type] = row[crime_type]
            else:
                crime_remap_counts[equiv_crime_type] += row[crime_type]

        for k in crime_remap_counts:
            combined_df["city"].append(row["city"])
            combined_df["date"].append(row["date"])
            combined_df["crime_type"].append(k)
            combined_df["crime_count"].append(crime_remap_counts[k])
            combined_df["daily_cases"].append(daily_cases)
            combined_df["total_cases"].append(total_cases)

    combined_df = pd.DataFrame(combined_df)
    combined_df.to_csv("parsed_data/combined_cases_crime_equivalent_daily.csv", index=False)


def combine_parsed_dfs_two(remap_lu: dict):
    """
    month_year, city, monthly_cases_absolute, monthly_cases_normalized,
    crime_types_absolute, crime_types_normalized...
    """

    memphis_df = pd.read_csv("parsed_data/memphis_crime.csv")
    memphis_df.columns = [v.lower() for v in memphis_df.columns]
    chicago_df = pd.read_csv("parsed_data/chicago_crime.csv")
    chicago_df.columns = [v.lower() for v in chicago_df.columns]
    boston_df = pd.read_csv("parsed_data/boston_crime.csv")
    boston_df.columns = [v.lower() for v in boston_df.columns]
    covid_df = pd.read_csv("parsed_data/daily_covid_cases.csv")

    # Get Covid Data in a way we can hash easy for below
    covid_case_lu = {c: {} for c in covid_df["city"].unique().tolist()}
    for i, row in covid_df.iterrows():
        if row["date"] not in covid_case_lu:
            covid_case_lu[row["date"]] = row["date"]
            covid_case_lu[row["date"]] = {c: None for c in covid_df["city"].unique().tolist()}
        covid_case_lu[row["date"]][row["city"]] = {"daily_cases": row["daily_cases"], "total_cases": row["total_cases"]}

    combined_df = {"city": [], "date": [], "crime_type": [], "crime_count": [], "daily_cases": [], "total_cases": []}

    # Memphis
    memphis_crime_types = memphis_df.columns.tolist()
    memphis_crime_types.remove("city")
    memphis_crime_types.remove("date")
    for i, row in memphis_df.iterrows():
        try:
            daily_cases = covid_case_lu[row["date"]][row["city"]]["daily_cases"]
        except KeyError:
            daily_cases = 0
        try:
            total_cases = covid_case_lu[row["date"]][row["city"]]["total_cases"]
        except KeyError:
            total_cases = 0

        for crime_type in memphis_crime_types:
            combined_df["city"].append(row["city"])
            combined_df["date"].append(row["date"])
            combined_df["crime_type"].append(crime_type)
            combined_df["crime_count"].append(row[crime_type])
            combined_df["daily_cases"].append(daily_cases)
            combined_df["total_cases"].append(total_cases)

    # Chicago
    chicago_crime_types = chicago_df.columns.tolist()
    chicago_crime_types.remove("city")
    chicago_crime_types.remove("date")
    for i, row in chicago_df.iterrows():
        try:
            daily_cases = covid_case_lu[row["date"]][row["city"]]["daily_cases"]
        except KeyError:
            daily_cases = 0
        try:
            total_cases = covid_case_lu[row["date"]][row["city"]]["total_cases"]
        except KeyError:
            total_cases = 0

        crime_remap_counts = {}
        for crime_type in chicago_crime_types:
            equiv_crime_type = remap_lu[row["city"]][crime_type]
            if equiv_crime_type not in crime_remap_counts:
                crime_remap_counts[equiv_crime_type] = row[crime_type]
            else:
                crime_remap_counts[equiv_crime_type] += row[crime_type]

        for k in crime_remap_counts:
            combined_df["city"].append(row["city"])
            combined_df["date"].append(row["date"])
            combined_df["crime_type"].append(k)
            combined_df["crime_count"].append(crime_remap_counts[k])
            combined_df["daily_cases"].append(daily_cases)
            combined_df["total_cases"].append(total_cases)

    # Boston
    boston_crime_types = boston_df.columns.tolist()
    boston_crime_types.remove("city")
    boston_crime_types.remove("date")
    for i, row in boston_df.iterrows():
        try:
            daily_cases = covid_case_lu[row["date"]][row["city"]]["daily_cases"]
        except KeyError:
            daily_cases = 0
        try:
            total_cases = covid_case_lu[row["date"]][row["city"]]["total_cases"]
        except KeyError:
            total_cases = 0

        crime_remap_counts = {}
        for crime_type in boston_crime_types:
            equiv_crime_type = remap_lu[row["city"]][crime_type]
            if equiv_crime_type not in crime_remap_counts:
                crime_remap_counts[equiv_crime_type] = row[crime_type]
            else:
                crime_remap_counts[equiv_crime_type] += row[crime_type]

        for k in crime_remap_counts:
            combined_df["city"].append(row["city"])
            combined_df["date"].append(row["date"])
            combined_df["crime_type"].append(k)
            combined_df["crime_count"].append(crime_remap_counts[k])
            combined_df["daily_cases"].append(daily_cases)
            combined_df["total_cases"].append(total_cases)

    combined_df = pd.DataFrame(combined_df)
    combined_df.to_csv("parsed_data/combined_cases_crime_equivalent_daily.csv", index=False)


def normalize_and_combine_single(case_df: pd.DataFrame, crime_df: pd.DataFrame, city_name: str,
                                 crime_equiv_lookup: dict):

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
    combined_df = crime_df.merge(sub_case_df, on=["date", "city"])

    city_crime_types = list(combined_df.columns)
    city_crime_types.remove("date")
    city_crime_types.remove("city")
    city_crime_types.remove("daily_cases")
    city_crime_types.remove("total_cases")

    # # Floor Date By Month/Sum Crime/Case Counts
    combined_df["date"] = pd.to_datetime(combined_df.date).dt.to_period('M').dt.to_timestamp()
    temp_agg = {k: 'sum' for k in city_crime_types}
    temp_agg["daily_cases"] = "sum"
    combined_df = combined_df.groupby(["date"], as_index=False).agg(temp_agg)

    ## Remap and re-sum if applicable
    combined_df.columns = combined_df.columns.str.lower()
    new_crime_types = list(crime_equiv_lookup["Memphis"].keys())

    equiv_df = [["city", "month_year", "monthly_cases"] + new_crime_types]

    for i, row in combined_df.iterrows():
        monthly_new_crime_counts = {k: 0 for k in new_crime_types}
        for native_crime_type in city_crime_types:
            try:
                equiv_crime = crime_equiv_lookup[city_name][native_crime_type.lower()]
                monthly_new_crime_counts[equiv_crime] += row[native_crime_type.lower()]
            except KeyError:
                continue
        new_crime_counts = [monthly_new_crime_counts[k] for k in new_crime_types]
        equiv_df.append([city_name, row["date"], row["daily_cases"]] + new_crime_counts)

    equiv_df = pd.DataFrame(data=equiv_df[1:], columns=equiv_df[0])

    # # Min/Max Normalization
    for k in ["monthly_cases"] + new_crime_types:
        k_max = equiv_df[k].max()
        equiv_df[k] = equiv_df[k].apply(lambda x: x / k_max)

    return equiv_df


def main():

    # determine_crime_classification()

    crime_remap_lookup = make_remap_lu()

    # combine_parsed_dfs(remap_lookup)

    # Load in dataframes
    covid_case_df = pd.read_csv("parsed_data/daily_covid_cases.csv")
    memphis_crime_df = pd.read_csv("parsed_data/memphis_crime.csv")
    chicago_crime_df = pd.read_csv("parsed_data/chicago_crime.csv")
    boston_crime_df = pd.read_csv("parsed_data/boston_crime.csv")

    memphis_crime_df_norm = normalize_and_combine_single(covid_case_df, memphis_crime_df, city_name="Memphis",
                                                         crime_equiv_lookup=crime_remap_lookup)

    chicago_crime_df_norm = normalize_and_combine_single(covid_case_df, chicago_crime_df, city_name="Chicago",
                                                         crime_equiv_lookup=crime_remap_lookup)

    boston_crime_df_norm = normalize_and_combine_single(covid_case_df, boston_crime_df, city_name="Boston",
                                                        crime_equiv_lookup=crime_remap_lookup)

    combined_df = pd.concat([memphis_crime_df_norm, chicago_crime_df_norm, boston_crime_df_norm])

    combined_df.to_csv("parsed_data/combined_cases_crime_equivalent_monthly_normalized.csv", index=False)



if __name__ == "__main__":

    main()

