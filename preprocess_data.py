from os import path

import pandas as pd


def read_data() -> pd.DataFrame:
    filename = path.join(path.dirname(__file__), 'train.csv')
    df = pd.read_csv(filename)

    # Use "id" column as index
    df.set_index("id", inplace=True)
    # Drop 188 rows that don't have host_identity_verified or host_has_profile_pic
    df.drop(df[(df["host_identity_verified"].isna()) |
               (df["host_has_profile_pic"].isna())].index, inplace=True)
    # Drop 135 rows that don't have the number of beds or have 0 beds
    df.drop(df[(df["beds"].isna()) | (df["beds"] == 0)].index, inplace=True)
    # Drop 958 that don't have a valid zipcode
    df.drop(df[~df["zipcode"].str.match(
        r"^[0-9]{5}", na=False)].index, inplace=True)
    # Drop unneded columns
    columns = ['bed_type', 'cancellation_policy', 'description', 'first_review',
               'host_response_rate', 'last_review', 'name', 'neighbourhood', 'thumbnail_url']
    df.drop(axis=1, columns=columns, inplace=True)
    # Fill some columns with the mean
    for col in ["review_scores_rating"]:
        df[col].fillna(df[col].mean(), inplace=True)
    # Fill some columns with zero
    for col in ["bathrooms", "bedrooms"]:
        df[col].fillna(0, inplace=True)
    # Transform columns to correct data types
    for col in ['host_has_profile_pic', 'host_identity_verified', 'instant_bookable']:
        df[col] = df[col].apply(lambda x: x == "t")
    df["beds"] = df["beds"].astype(int)
    df["bedrooms"] = df["bedrooms"].astype(int)
    df["zipcode"] = df["zipcode"].str[:5].astype(int)
    df["host_since"] = pd.to_datetime(df["host_since"])

    return df


def extract_list_val(s):
    for c in ['{', '}', '"']:
        s = s.replace(c, '')
    for c in ['/', ':', ' ', '-', '.', '&', ')', '(', '\'']:
        s = s.replace(c, '_')
    s = s.replace('matress', 'mattress')
    return s.split(',')


def explode_amenities(amenities: pd.DataFrame) -> pd.DataFrame:
    # Split amenities into a Python list
    column_list = amenities.apply(extract_list_val)
    freq_df = column_list.explode("amenities").value_counts().to_frame()
    # Discard amenities that start with "translation_missing"
    # and amenities with a frequency lower than 10,000
    selected_am = freq_df[(~freq_df.index.str.match("translation_missing")) &
                          (freq_df["amenities"] > 10000)].index
    # Create columns
    am_df = pd.DataFrame()
    for am in selected_am:
        am_df[am] = column_list.apply(lambda x: am in x)

    return am_df


if __name__ == "__main__":
    repo_root = path.dirname(__file__)

    data = read_data()
    print(" --------- Data")
    print(data.info())

    amenities = explode_amenities(data["amenities"])
    print(" --------- Amenities")
    print(amenities.info())

    print("Writing file 'airbnb_amenities_clean.csv' in the repo root")
    filename = path.join(repo_root, 'airbnb_amenities_clean.csv')
    amenities.to_csv(filename)

    print("Writing file 'airbnb_clean.csv' in the repo root without the 'amenities' column")
    data.drop(axis=1, columns=['amenities'], inplace=True)
    filename = path.join(repo_root, 'airbnb_clean.csv')
    data.to_csv(filename)
