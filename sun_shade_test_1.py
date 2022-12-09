# imports packages

import geopandas as gpd
import osmnx as ox
import pybdshadow
import pandas as pd
import numpy as np
import transbigdata as tbd
import networkx as nx

from suncalc import get_times
from shapely.geometry import MultiPolygon

from pybdshadow import bdshadow_sunlight
from pybdshadow.preprocess import bd_preprocess
from pybdshadow.analysis import get_timetable, cal_sunshine, cal_sunshadows, cal_shadowcoverage, count_overlapping_features


def sun_shade_solar_panel(lat=40.775, lng=-73.96, day='2022-12-16', dist=50, roof=True, precision = 10800, accuracy=1, padding=1800): #Attention distance!
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
    roof : bool
        whether to calculate roof shadow.
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
    
    # import data from OSM
    tags = {"building": True, 'height': True, 'ele': True}
    center_point = (lat, lng)
    raw_buildings = ox.geometries_from_point(center_point, tags=tags, dist=dist)
    
    # Data preprocessing
    raw_buildings.reset_index(inplace = True) # remove index
    buildings = raw_buildings[['height','geometry']] # new dataframe with only the col needed
    buildings['building_id'] = range(len(buildings))
    buildings = buildings[buildings['height'].notna()] # remove na of height
    buildings['height'] = buildings['height'].str.split(';') # split heights when there are more than one
    buildings['height'] = buildings['height'].apply(lambda x: max(x)) # select the heighest value
    buildings['height']= pd.to_numeric(buildings['height'], errors='coerce')
       
    # Calculate sunshine time on the building roof or on the ground regarding the roof parameter
    sunshine = pybdshadow.cal_sunshine(buildings,
                                   day=day,
                                   roof=roof,
                                   accuracy=accuracy,
                                   precision=precision) # one mesure every 3 hours per day
    
    return sunshine
