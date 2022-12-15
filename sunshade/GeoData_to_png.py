# Function to transform GeoDataFrame to png => for a gif
# Giving a folder of GeoData
# Return image in the targe folder (need to be made before)

# imports
import shapely.geometry
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def GeoData_to_png(path='./raw-data/GeoData', Image_Storage_directory='./raw-data/Images'):

    dir_list = os.listdir(path)

    for index, file_name in enumerate(dir_list):
        # read file to df
        df = pd.read_csv(f'{path}/{file_name}')

        # decode geometry columns as strings back into shapely objects
        for c in ["geometry"]:
            df[c] = df[c].apply(shapely.wkt.loads)

        gdf = gpd.GeoDataFrame(df)

        #Visualize sunshine time using matplotlib
        fig = plt.figure(1,(10,5))
        ax = plt.subplot(111)
        #define colorbar
        cax = plt.axes([0.05, 0.33, 0.02, 0.3])
        plt.title('Hour')
        #plot the sunshine time
        gdf.plot(ax = ax,cmap = 'plasma',column ='Hour',alpha = 1,legend = True,vmin = 0, vmax = 14, cax = cax)
        #Buildings
        #buildings.plot(ax = ax,edgecolor='k',facecolor=(0,0,0,0))
        plt.sca(ax)
        plt.title(f'Sunshine time /{file_name.rsplit("_20", 1)[1]}')

        fname = f'{Image_Storage_directory}/{file_name[:-4]}.png'
        plt.savefig(fname, format ='png')
        fig.clear()
        print(f"Saved figure {index+1} of {len(dir_list)}")

    return print('Images are ready')

if __name__ == "__main__":
    GeoData_to_png()
