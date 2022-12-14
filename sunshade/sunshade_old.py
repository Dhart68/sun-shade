# imports packages

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

from sun_shade_lib import solar_radiation_requests # to do : creat sun_shade_lib and move the fonction in it


def sun_shade_solar_panel(lat=40.775, lng=-73.96, dist=50, precision = 10800, accuracy=1, padding=1800): #Attention distance!
    '''
    Calculate the sunshine time in given date for a position, taking into account buildings arount a circle of dist in meter

    Parameters
    --------------------
    lat : float
        latitude
    lng : float
        longitude  
    day : str
        the day to calculate the sunshine   
    dist : int
        distance around the define point of interest in meter, limit the surround buildings used in the analysis  
    precision : number
        time precision(s)
    accuracy : number
        size of grids. Produce vector polygons if set as `vector` 
    padding : number
        padding time before and after sunrise and sunset

    Return
    ----------
    grids : GeoDataFrame
        grids generated by TransBigData in study area, each grids have a `time` column store the sunshine time

    '''
    # import data from NASA
    df_solar_radiation_year = solar_radiation_requests(lat, lng)
    
    # import data from OSM
    tags = {"building": True, 'height': True, 'ele': True}
    #center_point = (lat, lng)
    #raw_buildings = ox.geometries_from_point(center_point, tags=tags, dist=dist)
    # select only buildings south of the center point (1 degree lat = 111 111 m)
    if lat>0:
        optimized_point = (lat-(round(dist/111111,4)*0.8), lng)
    else:
        optimized_point = (lat+(round(dist/111111,4)*0.8), lng)
        
    raw_buildings = ox.geometries_from_point(optimized_point, tags=tags, dist=dist)
    
    # Data preprocessing
    raw_buildings.reset_index(inplace = True) # remove index
    buildings = raw_buildings[['height','geometry']] # new dataframe with only the col needed
    buildings['building_id'] = range(len(buildings))
    buildings = buildings[buildings['height'].notna()] # remove na of height
    buildings['height'] = buildings['height'].str.split(';') # split heights when there are more than one
    buildings['height'] = buildings['height'].apply(lambda x: max(x)) # select the heighest value
    buildings['height']= pd.to_numeric(buildings['height'], errors='coerce')
       
    # List of day of the year 2021 (every sundays)
    start = '2021-01-01'
    end = '2021-12-26'
    day_list=pd.date_range(start, end,4) # 52 for all year, use 2, 4, 8 to test
    
    # Loop on the list of the day
    # dataframe preparation
    selected_days=pd.DataFrame()
    selected_days['date'] = day_list
    selected_days['roof']=0
    selected_days['sunshadow']=0 # init col sunshine   
    
    # Test if selected position is on a roof
    p=Point(lng, lat)
    building_test = buildings['geometry'].apply(lambda x: x.intersects(p))
    if building_test.any()==True: 
        roof = True
    else:
        roof = False
    
    # Calculate sunshine time on the building roof or on the ground regarding the roof parameter
    # => substraction of the time mesured in shadow to the daylight time (sunset - sunrise) 
    for i in range(len(selected_days)):
        day=str(day_list[i])
        day[:10]
        sunshine = pybdshadow.cal_sunshine(buildings,
                                    day=day,
                                    roof=roof,
                                    accuracy=accuracy,
                                    precision=precision)
        # intersection point with polygon : point p = lng/lat chosen, polygon = area of calculated time of sunshine
        sunshine['intersect'] = sunshine['geometry'].apply(lambda x: x.intersects(p))
        df_test = sunshine[sunshine['intersect'] == True]
        # append the dataframe : 
        selected_days['roof'][i]=roof
        selected_days['sunshadow'][i]=(np.mean(df_test['Hour'])) 
        
    # Merge info from API and Cal_sunshine 
    selected_days # TO DO search data in API and merge it
        
    return selected_days
