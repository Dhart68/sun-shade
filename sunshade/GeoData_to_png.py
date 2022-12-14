# Function to transform GeoDataFrame to png => for a gif
# Giving a folder of GeoData
# Return image in the targe folder (need to be made before)

# imports
import shapely.geometry
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def GeoData_to_png(GeoData_directory='./raw-data/GeoData', Image_Storage_directory='./raw-data/Images'):
    
    for file_name in GeoData_directory: # todo
        # read file to df
        df = pd.read_csv(f'{GeoData_directory}/{file_name}')
        
        # decode geometry columns as strings back into shapely objects
        for c in ["geometry"]:
            df[c] = df[c].apply(shapely.wkt.loads)
        
        gdf = gpd.GeoDataFrame(df)
        
        #Visualize sunshine time using matplotlib
        fig = plt.figure(1,(10,5))
        ax = plt.subplot(111)
        #define colorbar
        cax = plt.axes([0.15, 0.33, 0.02, 0.3])
        plt.title('Hour')
        #plot the sunshine time
        gdf.plot(ax = ax,cmap = 'plasma',column ='Hour',alpha = 1,legend = True,cax = cax) # to do = defining a fixed legend
        #Buildings
        #buildings.plot(ax = ax,edgecolor='k',facecolor=(0,0,0,0))
        plt.sca(ax)
        plt.title('Sunshine time')
        
        fname = f'{Image_Storage_directory}{file_name[:-4]}.png'
        fname
        plt.savefig(fname, format ='png', dpi=150)

    return print('Images are ready')