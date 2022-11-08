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


def main():

    determine_crime_classification()


if __name__ == "__main__":

    main()

