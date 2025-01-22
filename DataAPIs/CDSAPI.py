import numpy as np
import pandas as pd
import cdsapi
import pygrib
import xarray as xr
from Utils import GRIBUtils


'''
CDS API class for loading data from CDS
Requirements: '.cdsapirc' fle in home directory, containing CDS url and key

Datasets available at: https://cds.climate.copernicus.eu/datasets
    * Select requested values
    * Copy request from 'Show API request code' section
    
Docs: https://cds.climate.copernicus.eu/how-to-api
'''
class CDSAPI:
    def __init__(self):
        self.client = cdsapi.Client()

    def retrieve(self, dataset: str, request: dict, target: str) -> xr.Dataset:
            return self.client.retrieve(dataset, request, target)

############### CODE Example ##########################################################################################

if __name__ == "__main__":
    print("Example of loading data from CDS")
    cds = CDSAPI()
    dataset = "reanalysis-era5-land"
    request = {
        "variable": ["2m_temperature"],
        "year": "2021",
        "month": "01",
        "day": ["01"],
        "time": [
        "00:00", "01:00", "02:00",
        "03:00", "04:00", "05:00",
        "06:00", "07:00", "08:00",
        "09:00", "10:00", "11:00",
        "12:00", "13:00", "14:00",
        "15:00", "16:00", "17:00",
        "18:00", "19:00", "20:00",
        "21:00", "22:00", "23:00"
    ],
        "data_format": "grib",
        "download_format": "archive"
    }
    target = "../Data/era5-jan-01.grib"

    cds.retrieve(dataset, request, target)

    df = GRIBUtils.open_grib_as_dataframe("../Data/download.grib")
    print(df.head(10))

#######################################################################################################################