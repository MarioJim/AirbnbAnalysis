from os import path
from typing import Tuple
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn

sys.path.append('..')
from read_data import read_airbnb_df, read_amenities_df  # nopep8


def correlation_matrix(df: pd.DataFrame, title: str, filename: str,
                       size: Tuple[float, float]):
    corr = df.corr().round(2)
    plt.figure()
    plt.title("Correlation matrix: " + title)
    sn.heatmap(corr, annot=True, vmin=-1, vmax=1, cmap="coolwarm",
               xticklabels=True, yticklabels=True)
    plt.xticks(rotation=45, ha="right")
    plt.gcf().set_size_inches(size[0], size[1])
    plt.gcf().tight_layout(pad=2)
    plt.savefig(filename)


if __name__ == "__main__":
    graphs_folder = path.join(path.dirname(__file__), 'graphs')

    df = read_airbnb_df()
    df_am = read_amenities_df()

    # Data correlation matrix
    df_mtx_name = path.join(graphs_folder, 'corrmtx_data.png')
    correlation_matrix(df, "Airbnb data", df_mtx_name, (12, 8))

    # Amenities correlation matrix
    df_am_mtx_name = path.join(graphs_folder, 'corrmtx_am.png')
    correlation_matrix(df_am, "Airbnb amenities", df_am_mtx_name, (18, 12))

    # Data + Amenities correlation matrix
    df_concat = pd.concat([df, df_am], axis=1)
    df_concat_mtx_name = path.join(graphs_folder, 'corrmtx_concat.png')
    correlation_matrix(df_concat, "Airbnb data and amenities",
                       df_concat_mtx_name, (27, 18))
