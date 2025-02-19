from datetime import datetime, timezone
from typing import List

import pandas as pd
import h5py
import matplotlib
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np



def load_hdf(file_path: str) -> pd.DataFrame():
    # Load the HDF5 file
    with h5py.File(file_path, "r") as f:
        print("Available datasets:", list(f.keys()))  # Check available datasets

        # Load column labels
        columns = f["data"]["block0_items"][:].astype(str)  # Convert bytes to string

        # Load main data values
        values = f["data"]["block0_values"][:]

        # Load index
        index_0 = f["data"]["axis0"][:]
        index_1 = f["data"]["axis1_label0"][:].astype(str)  # Convert to string
    # Construct DataFrame
    df = pd.DataFrame(values, columns=columns, index=index_1)
    # Display the DataFrame
    print(df.head())
    print(df.shape)  # Check the number of rows/columns

def load_hdf_pandas(file_path: str) -> pd.DataFrame():
    return pd.read_hdf(file_path)

def abc_predictions_file_to_dataframe(file_path):
    with h5py.File(file_path, 'r') as hdf:
        # Extracting datasets
        block0_items = hdf['data']['block0_items'][:]  # Column name: 'start_date'
        block0_values = hdf['data/block0_values'][:]  # Column values

        block1_items = hdf['data/block1_items'][:]  # Column names: 'lat', 'lon', 'pred'
        block1_values = hdf['data/block1_values'][:]  # Column values

        # Decoding bytes to string (if needed)
        block0_items = [item.decode() for item in block0_items]
        block1_items = [item.decode() for item in block1_items]

        # Debugging: Print shapes
        print(f"block1_items (column names): {block1_items}")
        print(f"block1_values shape: {block1_values.shape}")

        # Creating the DataFrame
        df = pd.DataFrame(block1_values, columns=block1_items)

        # Adding the 'start_date' column
        # Convert to seconds
        seconds_timestamp = block0_values[0][0] / 1e9
        # Convert to date
        date = datetime.fromtimestamp(seconds_timestamp, tz=timezone.utc).date()
        df['start_date'] = date
        return df

def get_min_max_dates(df: pd.DataFrame, date_column: str) -> tuple:
    """
    Get the minimum and maximum dates in a DataFrame.

    :param df: Pandas DataFrame containing the date column.
    :param date_column: Name of the column containing dates.
    :return: Tuple containing (min_date, max_date).
    """
    min_date = df[date_column].min()
    max_date = df[date_column].max()
    return min_date, max_date


def show_measurement_on_map(data_matrix, title, vmax):
    """Show sequential measurements on the U.S. map in an matplotlib.animation plot

    Parameters
    ----------
    data_matrix: array of formatted data matrices (see get_data_matrix)

    title: array of titles to accompany the data matrices

    vmax: Maximum value on colorbar. Minimum is 0.
    """
    # Set figure
    fig = plt.figure(figsize=(9, 6))
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.PlateCarree())

    # Draw coastlines, US states
    ax.coastlines(linewidth=0.2, color='black')  # add coast lines
    ax.add_feature(cfeature.STATES)  # add US states
    ax.set_yticks(np.arange(25, 50 + 1, 5), crs=ccrs.PlateCarree())
    ax.set_xticks(np.arange(-125, -67 + 1, 8), crs=ccrs.PlateCarree())
    lats = np.linspace(26, 50, data_matrix[0].shape[0] + 1)
    lons = np.linspace(-125, -68, data_matrix[0].shape[1] + 1)
    color_map = 'RdBu_r'
    plot = ax.pcolormesh(lons + 0.5, lats - 0.5, data_matrix[0],
                         vmin=0, vmax=vmax,
                         cmap=color_map, snap=True)
    cb = plt.colorbar(plot, fraction=0.02, pad=0.04)

    def animate(i):
        plot.set_array(data_matrix[i].ravel())
        plt.title(title[i])
        return plot

    ani = animation.FuncAnimation(
        fig, animate, frames=len(data_matrix), interval=700, blit=False, repeat=False)
    return ani

def get_data_matrix(data, values):
    """Get pandas dataframe with (lat, lon, values) ready for plotting

    If there is more than one value per (lat, lon) grid point, the values will be averaged.
    This is especially useful for calculating daily/monthly/yearly averages.

    Parameters
    ----------
    data: pd.DataFrame with (lat, lon, values) format

    values: Name of the 'values' column
    """
    # Average if more than one data point per (lat, lon) pair
    data_aux = data[["lat", "lon", values]].groupby(by=["lat", "lon"], as_index=False).agg(np.mean)
    data_pivot = data_aux.pivot(index='lat', columns='lon', values=values)
    data_matrix = data_pivot.values
    data_matrix = np.ma.masked_invalid(data_matrix)
    return data_matrix

def hdf_to_csv(hdf_path: str, destination_path: str):
    df = pd.read_hdf(hdf_path)
    df.to_csv(destination_path, index=False)

def filter_hdf_by_years(hdf_path: str, date_column: str, years: List[int]) -> pd.DataFrame():
    df = pd.read_hdf(hdf_path)
    df_filtered = df[df[date_column].dt.year.isin(years)]
    return df_filtered


if __name__ == "__main__":
    abc_predictions_file_to_dataframe("/Users/shemiperetz/PycharmProjects/subseasonal_toolkit/models/climpp/submodel_forecasts/climpp-lossrmse_yearsall_margin10/us_tmp2m_1.5x1.5_12w/us_tmp2m_1.5x1.5_12w-20150101.h5")