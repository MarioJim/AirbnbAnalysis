from os import path
import sys

import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import skew, kurtosis
import seaborn as sns

sys.path.append('..')
from read_data import read_airbnb_df  # nopep8


def stats_analysis(column: pd.DataFrame, title: str, xlbl: str, binwidth: int,
                   log_scale: bool, filename: str):
    # Histogram
    plt.figure()
    plt.title("Histogram: " + title)
    sns.histplot(data=column, binwidth=binwidth, log_scale=log_scale)
    plt.xlabel(xlbl)
    plt.savefig(filename)

    print("Mean: ", column.mean())
    print("Variance: ", column.var())
    print("StdDev: ", column.std())
    print("Symmetry: ", skew(column))
    print("Kurtosis: ", kurtosis(column))
    print()


if __name__ == "__main__":
    graphs_folder = path.join(path.dirname(__file__), 'graphs')

    df = read_airbnb_df()

    # Reviews histogram
    hist_reviews = path.join(graphs_folder, 'hist_reviews.png')
    stats_analysis(df["number_of_reviews"],
                   "Number of reviews", "Reviews", None, False, hist_reviews)

    # Review scores histogram
    hist_rev_scores = path.join(graphs_folder, 'hist_rev_scores.png')
    stats_analysis(df[df["number_of_reviews"] != 0]["review_scores_rating"],
                   "Review scores rating", "Score", 2, False, hist_rev_scores)
