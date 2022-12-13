import pandas as pd

def data_preprocessing(raw_buildings):
    # Data preprocessing
    raw_buildings.reset_index(inplace = True) # remove index
    buildings = raw_buildings[['height','geometry']] # new dataframe with only the col needed
    buildings['building_id'] = range(len(buildings))
    buildings = buildings[buildings['height'].notna()] # remove na of height
    buildings['height'] = buildings['height'].str.split(';') # split heights when there are more than one
    buildings['height'] = buildings['height'].apply(lambda x: max(x)) # select the heighest value
    buildings['height']= pd.to_numeric(buildings['height'], errors='coerce')
    
    return buildings
