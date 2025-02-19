import numpy as np
import pandas as pd
import cdsapi
import pygrib
import xarray as xr
import netCDF4 as nc

def open_grib_as_dataframe(path: str) -> pd.DataFrame:
    ds = xr.open_dataset(path, engine='cfgrib')
    return ds.to_dataframe()


def process_grib_to_df(grib_file_path: str) -> pd.DataFrame:
  # Open the GRIB file
  ds = xr.open_dataset(grib_file_path)

  # Convert to DataFrame
  df = ds.to_dataframe().reset_index()

  # Change specific column names
  df = df.rename(columns={
      'time': 'Predicted_at_time',
      'valid_time': 'Date',
      "t2m": 'Temperature',
      'latitude': 'Latitude',
      'longitude': 'Longitude'
  })

  df['Temperature'] = k2c(df['Temperature'])
  df['Predicted_at_time'] = df['Predicted_at_time'].dt.date
  df['Date'] = df['Date'].dt.date

  return df.dropna()

def process_nc_to_df(nc_file_path: str) -> pd.DataFrame:
  # nc_file = nc.Dataset(nc_file_path)
  nc_file = xr.open_dataset(nc_file_path)
  df = nc_file.to_dataframe().reset_index()

  # Change specific column names
  df = df.rename(columns={
      'valid_time': 'Date',
      "t2m": 'Temperature',
      'latitude': 'Latitude',
      'longitude': 'Longitude'
  })

  df['Temperature'] = k2c(df['Temperature'])
  df['Date'] = df['Date'].dt.date

  return df

def k2c(k):
  c = k - 273.15
  return c


if __name__ == '__main__':
    process_nc_to_df("../Data/era5-2021-jan.nc")