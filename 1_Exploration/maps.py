import sys
from os import path

import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append('..')
from read_data import read_airbnb_df  # nopep8


def draw_map(df: pd.DataFrame, title: str, filename: str):
    lats = df.groupby(["city"])["latitude"].mean()
    lons = df.groupby(["city"])["longitude"].mean()
    freqs = df["city"].value_counts().sort_index()

    fig = plt.figure()
    fig.set_size_inches(10, 6)
    ax = fig.add_subplot(1, 1, 1, projection=crs.PlateCarree())

    ax.stock_img()
    ax.coastlines()
    ax.add_feature(cfeature.STATES)
    ax.set_extent([-130, -66, 22, 56], crs=crs.PlateCarree())

    plt.title("Map: " + title)
    for city, lat, lon, freq in zip(freqs.index.tolist(), lats, lons, freqs):
        lbl = "{} ({} listings)".format(city, freq)
        plt.scatter(lon, lat, 0.03 * freq, label=lbl,
                    transform=crs.PlateCarree())
    plt.legend(loc="upper left")
    plt.subplots_adjust(left=0.05, right=0.95)
    plt.savefig(filename)


if __name__ == "__main__":
    graphs_folder = path.join(path.dirname(__file__), 'graphs')

    df = read_airbnb_df()

    # All Airbnb listings
    all_map_name = path.join(graphs_folder, 'map_all.png')
    draw_map(df, "All Airbnb listings", all_map_name)
