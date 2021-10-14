import sys

import pandas as pd
from scipy.stats import shapiro, kstest, anderson

sys.path.append('..')
from read_data import read_airbnb_df  # nopep8


def normality_tests(column: pd.DataFrame):
    sw = shapiro(column)
    print(f"Shapiro-Wilk test for normality: {sw}")
    ks = kstest(column, "norm")
    print(f"Kolmogorov-Smirnov test for normality: {ks}")
    a = anderson(column)
    print(f"Anderson-Darling test for normality: {a}")
    print()


if __name__ == "__main__":
    df = read_airbnb_df()

    # Reviews test
    normality_tests(df["number_of_reviews"])

    # Review scores test
    normality_tests(df[df["number_of_reviews"] != 0]["review_scores_rating"])
