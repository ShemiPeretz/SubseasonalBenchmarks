from subseasonal_data import downloader, data_loaders
import pandas as pd
import numpy as np
import calendar


from Utils import HDFUtils

'''
Subseasonal Data USA dataset API class for loading data from Subseasonal Data USA
Requirements: 'SUBSEASONALDATA_PATH' env variable directing to desired data repository path

Docs: https://github.com/microsoft/subseasonal_data/blob/main/examples/Examples.ipynb
'''

class SubseasonalDataUsaAPI:
    def __init__(self):
        self.data_loaders = data_loaders
        self.downloader = downloader

    def list_subdirs(self):
        return self.downloader.list_subdir_files(data_subdir='combined_dataframes')

    def get_t2m_ground_truth(self):
        return data_loaders.get_ground_truth("us_precip", sync=True)

    def get_climatology(self):
        return data_loaders.get_climatology("us_precip")

    def get_ground_truth_in_years(self, years: list[int]) -> pd.DataFrame:
        df = self.get_t2m_ground_truth()
        # Filter for multiple years
        df_filtered = df[df['start_date'].dt.year.isin(years)]
        return df_filtered

    def get_percipitation_ground_truth(self):
        df = data_loaders.get_ground_truth("us_precip_1.5x1.5")
        return df

    def get_percipitation_in_years(self, years: list[int]) -> pd.DataFrame:
        df = self.get_percipitation_ground_truth()
        # Filter for a specific year
        df_filtered = df[df['start_date'].dt.year.isin(years)]
        return df_filtered




if __name__ == "__main__":
    data_api = SubseasonalDataUsaAPI()
    dataframes_path_prefix = "../Data/SubseasonalDataUsa/dataframes/"
    # # df = data_api.get_t2m_ground_truth()
    # # df.head()
    # # #
    # # df = HDFUtils.load_hdf("../Data/SubseasonalDataUsa/dataframes/gt-us_tmp2m-14d.h5")
    # # df.head()

    # df = data_api.get_percipitation_in_years([2015, 2016, 2017, 2108, 2019, 2020, 2021, 2022, 2023, 2024])
    # df.to_csv("../Data/SubseasonalDataUsa/dataframes/gt-us_precip_1.5x1.5-14d-2015-2024.csv", index=False)
    #
    # df= pd.read_csv("../Data/SubseasonalDataUsa/dataframes/gt-us_precip_1.5x1.5-14d-2015-2024.csv")
    # print(HDFUtils.get_min_max_dates(df, "start_date"))
    # df.head()

    # hdf_path = dataframes_path_prefix + "official_climatology-us_precip.h5"
    # csv_path = "../Data/SubseasonalDataUsa/dataframes/official_climatology-us_precip.csv"
    # HDFUtils.hdf_to_csv(hdf_path, csv_path)

    years = [2015, 2016, 2017, 2108, 2019, 2020, 2021, 2022, 2023, 2024]
    precip_hdf_path = dataframes_path_prefix + "iri-ecmwf-precip-all-us1_5-ef-forecast.h5"
    precip_csv_path = dataframes_path_prefix + "ecmwf-precip-us-ef-forecast.csv"
    tmp_hdf_path = dataframes_path_prefix + "iri-ecmwf-tmp2m-all-us1_5-ef-forecast.h5"
    tmp_csv_path = dataframes_path_prefix + "ecmwf-tmp2m-us-ef-forecast.csv"
    date_column = "start_date"

    precip_df = HDFUtils.filter_hdf_by_years(precip_hdf_path, date_column, years)
    tmp_df = HDFUtils.filter_hdf_by_years(tmp_hdf_path, date_column, years)

    precip_df.to_csv(precip_csv_path, index=False)
    tmp_df.to_csv(tmp_csv_path, index=False)
