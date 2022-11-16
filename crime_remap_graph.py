import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# G = nx.Graph()
# G.add_edges_from(
#     [('A', 'B'), ('A', 'C'), ('D', 'B'), ('E', 'C'), ('E', 'F'),
#      ('B', 'H'), ('B', 'G'), ('B', 'F'), ('C', 'G')])
#
# val_map = {'A': 1.0,
#            'D': 0.5714285714285714,
#            'H': 0.0}
#
# values = [val_map.get(node, 0.25) for node in G.nodes()]
#
# nx.draw(G, cmap = plt.get_cmap('jet'), node_color = values)
# plt.show()


def main():

    city = "Boston"
    crime_equiv_df = pd.read_csv("helper_data/crime_equiv - crime_equiv_v1.csv")
    crime_equiv_df = crime_equiv_df[crime_equiv_df["city"] == city]

    G = nx.Graph()
    edge_list = []
    for i, row in crime_equiv_df.iterrows():
        edge_list.append((row["native_cat"], row["equiv_cat"]))
    G.add_edges_from(edge_list)

    nx.draw(G, with_labels=True)
    plt.show()


if __name__ == "__main__":

    main()