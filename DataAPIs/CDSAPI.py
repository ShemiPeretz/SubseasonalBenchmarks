from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import cdsapi
import pygrib
import xarray as xr
from Utils import GRIBUtils
import netCDF4



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

    def retrieve_t2m_hourly_from_era5(self, years: [str], months: [str], days: [str], north: int, west: int, south: int, east: int,  target: str) -> xr.Dataset:
        dataset = "reanalysis-era5-land"
        request = {
            "variable": ["2m_temperature"],
            "year": years,
            "month": months,
            "day": days,
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
            "download_format": "archive",
            "area": [north, west, south, east]
        }
        return self.retrieve(dataset, request, target)

    def retrieve_t2m_daily_mean_from_era5(self, from_date: datetime.date, to_date: datetime.date, north: int, west: int, south: int, east: int,  target: str) -> xr.Dataset:
        years, months, days = self.dates_to_str_lists(from_date, to_date)

        dataset = "derived-era5-land-daily-statistics"
        request = {
            "variable": ["2m_temperature"],
            "year": "2021",
            "month": "01",
            "day": ["01","02"],
            "daily_statistic": "daily_mean",
            "time_zone": "utc+02:00",
            "frequency": "1_hourly",
            "area": [north, west, south, east]
        }
        return self.retrieve(dataset, request, target)

    def dates_to_str_lists(self, from_date: datetime, to_date: datetime):
        years = []
        months = []
        days = []

        # Loop through the date range
        current_date = from_date
        while current_date <= to_date:
            if str(current_date.year) not in years:
                years.append(str(current_date.year))
            if str(current_date.month) not in months:
                months.append(str(current_date.month))
            if str(current_date.day) not in days:
                days.append(str(current_date.day))

            current_date += timedelta(days=1)  # Move to the next day

        return years, months, days


############### CODE Example ##########################################################################################

if __name__ == "__main__":
    print("Example of loading data from CDS")
    cds = CDSAPI()
    # dataset = "reanalysis-era5-land"
    # request = {
    #     "variable": ["2m_temperature"],
    #     "year": "2021",
    #     "month": "01",
    #     "day": ["01"],
    #     "time": [
    #     "00:00", "01:00", "02:00",
    #     "03:00", "04:00", "05:00",
    #     "06:00", "07:00", "08:00",
    #     "09:00", "10:00", "11:00",
    #     "12:00", "13:00", "14:00",
    #     "15:00", "16:00", "17:00",
    #     "18:00", "19:00", "20:00",
    #     "21:00", "22:00", "23:00"
    # ],
    #     "data_format": "grib",
    #     "download_format": "archive"
    # }
    # target = "../Data/era5-jan-01.grib"
    #
    # cds.retrieve(dataset, request, target)

    target = "../Data/era5-2021-jan.nc"
    # cds.retrieve_t2m_daily_mean_from_era5(datetime(2021, 1, 1), datetime(2021, 1, 1),
    #                                       35, 34, 29, 36, target)

    # df = GRIBUtils.open_grib_as_dataframe("../Data/era5-2021-jan-01.nc")
    # df = GRIBUtils.process_grib_to_df("../Data/download.grib")
    df = GRIBUtils.process_nc_to_df("../Data/era5-2021-jan.nc")
    print(df.head(10))

#######################################################################################################################