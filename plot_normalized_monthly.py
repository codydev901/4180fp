import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from typing import List

"""
Doc Doc Doc
"""


def plot_combined_df_crimes(combined_df: pd.DataFrame, display_crimes: List[str], crime_group: int,
                            do_show: bool = False):

    t_df = [["city", "month_year", "monthly_cases", "crime_type", "crime_frequency"]]

    for i, row in combined_df.iterrows():
        for crime_type in display_crimes:
            t_df.append([row["city"], row["month_year"], row["monthly_cases"], crime_type, row[crime_type]])

    t_df = pd.DataFrame(data=t_df[1:], columns=t_df[0])

    fig = px.line(t_df, x="month_year", y=["crime_frequency", "monthly_cases"], color="city", facet_col="crime_type",
                  title=f"Date vs. Normalized COVID Case and Crime Frequency For Crime Group:{crime_group+1}",
                  facet_col_wrap=1)

    did_set_legend = []
    # Legend & Lines
    for i, sub_trace in enumerate(fig.data):
        if not ((i+1) % 2):  # Monthly Cases
            sub_trace.line.dash = "dashdot"
            sub_trace.legendgroup = f"{sub_trace.legendgroup} COVID Cases"
            sub_trace.name = f"{sub_trace.name} COVID Cases"
        else:
            sub_trace.legendgroup = f"{sub_trace.legendgroup} Crime Frequency"
            sub_trace.name = f"{sub_trace.name} Crime Frequency"

        if sub_trace.name not in did_set_legend:
            sub_trace.showlegend = True
            did_set_legend.append(sub_trace.name)

    # Sub-Titles
    for anno in fig.layout.annotations:
        anno.text = anno.text.split("=", 1)[-1].strip()

    if do_show:
        fig.show()

    fig.write_image(f"plots/normalized_crime_plot_{crime_group+1}.png")


def main():

    combined_df = pd.read_csv("parsed_data/combined_cases_crime_equivalent_monthly_normalized.csv")

    crime_types = combined_df.columns.tolist()
    crime_types.remove("city")
    crime_types.remove("month_year")
    crime_types.remove("monthly_cases")
    crime_types.remove("family offense")

    for i in range(4):

        s_i = i*4
        e_i = s_i + 4

        plot_combined_df_crimes(combined_df, display_crimes=crime_types[s_i:e_i], crime_group=i)


if __name__ == "__main__":

    main()
