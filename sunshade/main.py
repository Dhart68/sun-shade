# imports packages
import os
import geopandas as gpd
import osmnx as ox
import pybdshadow
import pandas as pd
import numpy as np
import transbigdata as tbd
import networkx as nx

from suncalc import get_times
from shapely.geometry import MultiPolygon, Point

from pybdshadow import bdshadow_sunlight
from pybdshadow.preprocess import bd_preprocess
from pybdshadow.analysis import get_timetable, cal_sunshine, cal_sunshadows, cal_shadowcoverage, count_overlapping_features
from sunshade.registry import save_cloud, save_local
from sunshade import import_OSM, data_preprocessing
from sunshade.solar_radiation_requests import historical_solar_radiation
from sunshade.list_of_selected_days import list_of_selected_days

PACKAGE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DATA_DIR = os.path.join(PACKAGE_DIR, 'raw_data')


def sun_shade_solar_panel(lat=40.775, lng=-73.96,
                          dist=50,
                          precision = 10800,
                          accuracy=1,
                          padding=1800,
                          start = '2021-01-03', end = '2021-12-26',
                          n=2,
                          cloud=True): #Attention distance!
    '''
    Calculate the sunshine time in given date for a position, taking into account buildings arount a circle of dist in meter

    Parameters
    --------------------
    lat : float
        latitude
    lng : float
        longitude
    dist : int
        distance around the define point of interest in meter, limit the surround buildings used in the analysis
    precision : number
        time precision(s)
    accuracy : number
        size of grids. Produce vector polygons if set as `vector`
    padding : number
        padding time before and after sunrise and sunset
    start = date like '2021-01-03'
        first day of the time range
    end = date like '2021-12-03'
        last day of the time range
    n = int 2,minimum
        number of days

    Return
    ----------
    selected_days : pandas DataFrame
        sunshine regarding shadows and solar raidation regarding weather per day for the POI
    sunshine_all_date : Geopandas DataFrame
        grids generated by TransBigData in study area, each grids have a `time` column store the sunshine time


    '''
    # import data from NASA
    df_solar_radiation_year = historical_solar_radiation(lat, lng)

    # import data from OSM
    raw_buildings = import_OSM.import_OSM(lat=lat, lng=lng, dist=dist, lat_lag = 0.8)

    # Data preprocessing
    buildings = data_preprocessing.data_preprocessing(raw_buildings)

    # Loop on the list of the day

    day_list = list_of_selected_days(start = start, end = end, n=n)

    # Test if selected position is on a roof
    p=Point(lng, lat)
    building_test = buildings['geometry'].apply(lambda x: x.intersects(p))
    if building_test.any()==True:
        roof = True
    else:
        roof = False

    # results dataframe preparation
    selected_days=pd.DataFrame()
    selected_days['latitude'] = lat*np.ones(len(day_list))
    selected_days['longitude'] = lng*np.ones(len(day_list))
    selected_days['distance'] = dist*np.ones(len(day_list))
    selected_days['date'] = day_list
    selected_days['roof']=roof*np.ones(len(day_list))
    selected_days['sunshadow']=0 # init col sunshine
    selected_days['daylight_hour']=0
    selected_days['energy_absorbed']=0

    # Calculate sunshine time on the building roof or on the ground regarding the roof parameter
    # => substraction of the time mesured in shadow to the daylight time (sunset - sunrise)
    for i in range(len(selected_days)):
        day = str(selected_days.loc[i,'date'])[:10]
        sunshine = pybdshadow.cal_sunshine(buildings,
                                    day=day,
                                    roof=roof,
                                    accuracy=accuracy,
                                    precision=precision)

        # intersection point with polygon : point p = lng/lat chosen, polygon = area of calculated time of sunshine
        sunshine['intersect'] = sunshine['geometry'].apply(lambda x: x.intersects(p))
        df_test = sunshine[sunshine['intersect'] == True]
        selected_days.loc[i, 'sunshadow']=(np.mean(df_test['Hour']))

        #processing the time of daylight
        date = pd.to_datetime(day+' 12:45:33.959797119')
        times = get_times(date, lng, lat)
        date_sunrise = times['sunrise']
        date_sunset = times['sunset']
        selected_days.loc[i, 'daylight_hour'] = (date_sunset - date_sunrise).total_seconds() / 60 / 60 #(timestamp_sunset-timestamp_sunrise)/(1000000000*3600)

        # save the data for one day
        file_name_1 = os.path.join(RAW_DATA_DIR, f"Data_{lat}_{lng}_{dist}.csv")
        if i==0:
            selected_days.loc[[i],:].to_csv(file_name_1, mode='w', header=True)
        else:
            selected_days.loc[[i], :].to_csv(file_name_1, mode='a', header=False)

        if cloud:
            save_cloud(file_name_1, file_name_1,bucket_name="sunshade_data_bucket")

        # append the sunshine_all :
        sunshine['latitude'] = lat
        sunshine['longitude'] = lng
        sunshine['date'] = day
        # save the geodataframe for one day
        file_name_2 = os.path.join(RAW_DATA_DIR, f"Geodata_{lat}_{lng}_{day}.csv")
        sunshine.to_csv(file_name_2)
        if cloud:
            save_cloud(file_name_2, file_name_2,bucket_name="sunshade_data_bucket")

        print(f'Date : {day} is done')


    # Merge info from API and Cal_sunshine
    selected_days = selected_days.merge(df_solar_radiation_year, how='inner', on='date')

    # computing new variable "energy_absorbed"
    selected_days['energy_absorbed']=(selected_days['sunshadow']*selected_days['radiation'])/selected_days['daylight_hour']
    file_name_3 = os.path.join(RAW_DATA_DIR, f"Data_{lat}_{lng}_{dist}_all_days.csv")
    selected_days.to_csv(file_name_3)
    if cloud:
            save_cloud(file_name_3, file_name_3,bucket_name="sunshade_data_bucket")

    return selected_days

if __name__ == '__main__':
    print('The function is running with the default parameters')
    sun_shade_solar_panel(lat=40.764872246937635,  lng=-73.95399566857668,
                          dist=50,
                          precision = 10800,
                          accuracy=1,
                          padding=1800,
                          start = '2021-01-03', end = '2021-12-26',
                          n=4,
                          cloud=False)
