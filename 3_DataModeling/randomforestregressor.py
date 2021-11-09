import sys

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

sys.path.append('..')
from read_data import read_airbnb_df, read_amenities_df  # nopep8


def randomForestRegression(df: pd.DataFrame, column: str):
    X = df.drop(columns=[column, "property_type", "city",
                         "room_type", "host_since"])
    y = df[column]

    Xtrain, Xtest, ytrain, ytest = train_test_split(
        X, y, test_size=0.2, random_state=0)

    regressor = RandomForestRegressor(random_state=0, n_jobs=-1)
    regressor.fit(Xtrain, ytrain)
    ypred = regressor.predict(Xtest)

    print("Accuracy:", r2_score(ytest, ypred))
    print("MSE:", mean_squared_error(ytest, ypred))

    for perc in [0.05, 0.1, 0.15, 0.2]:
        top = ytest * (1 + perc)
        bot = ytest * (1 - perc)
        count = np.count_nonzero((bot < ypred) & (ypred < top))
        print(f"{100 * perc}%", f"{count / ypred.shape[0]:.5f}")


if __name__ == "__main__":
    df = read_airbnb_df()
    df_am = read_amenities_df()
    df_concat = pd.concat([df, df_am], axis=1)

    for min_rev in [1, 5, 10, 20]:
        df = df_concat[df_concat["number_of_reviews"] >= min_rev]
        print(f"Random forest with {min_rev} min reviews",
              f"({df.shape[0]} instances)")
        randomForestRegression(df, "review_scores_rating")
        print()
