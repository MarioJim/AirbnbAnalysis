import sys
from os import path

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append('..')
from read_data import read_airbnb_df  # nopep8


def graph_hist2d(x: pd.DataFrame, y: pd.DataFrame, title: str,
                 xlabel: str, ylabel: str, filename: str):
    plt.title("Histogram: " + title)
    plt.hist2d(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(filename)


if __name__ == "__main__":
    graphs_folder = path.join(path.dirname(__file__), 'graphs')

    df = read_airbnb_df()

    # Reviews vs review scores where there's at least 1 review
    reviews_vs_scores_name = path.join(graphs_folder, 'reviews_vs_scores.png')
    at_least_one_review_df = df[df["number_of_reviews"] >= 1]
    x = np.log10(at_least_one_review_df["number_of_reviews"])
    y = at_least_one_review_df["review_scores_rating"]
    graph_hist2d(x, y, "Reviews distribution on listings with at least one",
                 "Logarithm base 10 of the number of reviews",
                 "Average review score", reviews_vs_scores_name)
