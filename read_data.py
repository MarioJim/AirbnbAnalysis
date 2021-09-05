from os import path

import pandas as pd


def read_airbnb_df() -> pd.DataFrame:
    df_name = path.join(path.dirname(__file__), 'airbnb_clean.csv')
    return pd.read_csv(df_name).set_index("id")


def read_amenities_df() -> pd.DataFrame:
    df_am_name = path.join(path.dirname(__file__),
                           'airbnb_amenities_clean.csv')
    return pd.read_csv(df_am_name).set_index("id")
