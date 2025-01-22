import numpy as np
import pandas as pd
import cdsapi
import pygrib
import xarray as xr

def open_grib_as_dataframe(path: str) -> pd.DataFrame:
    ds = xr.open_dataset(path, engine='cfgrib')
    return ds.to_dataframe()



