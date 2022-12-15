import pandas as pd
from shapely.geometry import Polygon, LineString, Point

def data_preprocessing(raw_buildings):
    # Data preprocessing
    raw_buildings.reset_index(inplace = True) # remove index
    if 'height' not in raw_buildings.columns:
        raise Exception("\n\nWe could not find the height data for this location. Please choose another location.\n\n") 
    buildings = raw_buildings[['height','geometry']] # new dataframe with only the col needed
    buildings['building_id'] = range(len(buildings))
    buildings = buildings[buildings['height'].notna()] # remove na of height
    buildings = buildings[buildings['geometry'].apply(lambda x: (not isinstance(x, Point) and not isinstance(x, LineString)))]
    buildings['height'] = buildings['height'].str.split(';') # split heights when there are more than one
    buildings['height'] = buildings['height'].apply(lambda x: max(x)) # select the heighest value
    buildings['height']= pd.to_numeric(buildings['height'], errors='coerce')
    
    return buildings
