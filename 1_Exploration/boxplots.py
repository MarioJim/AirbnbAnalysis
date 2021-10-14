import sys
from os import path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append('..')
from read_data import read_airbnb_df  # nopep8


def graph_boxplots(df: pd.DataFrame, columns: str, title: str, filename: str):
    fig, axes = plt.subplots(1, len(columns))
    fig.suptitle("Boxplots: " + title)
    fig.tight_layout(pad=1.0)
    for i, lbl in enumerate(columns):
        axes[i].boxplot(df[lbl], labels=[lbl])
    plt.savefig(filename)


if __name__ == "__main__":
    graphs_folder = path.join(path.dirname(__file__), 'graphs')

    df = read_airbnb_df()

    # Main boxplot
    boxplot_main_name = path.join(graphs_folder, 'boxplot_main.png')
    graph_boxplots(df, ["log_price", "accommodates", "beds"],
                   "Main columns", boxplot_main_name)

    # Reviews boxplot
    boxplot_reviews_name = path.join(graphs_folder, 'boxplot_reviews.png')
    graph_boxplots(df, ["number_of_reviews", "review_scores_rating"],
                   "Reviews", boxplot_reviews_name)
