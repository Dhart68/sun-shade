# Visualize buildings and shadows using matplotlib
import pandas as pd
import geopandas as gpd
import pybdshadow
import matplotlib.pyplot as plt
import networkx as nx

from sunshade import import_OSM, data_preprocessing


def visualize_3d(lat=40.775, lng=-73.96, dist=100):
    # import data from OSM
    raw_buildings = import_OSM.import_OSM(lat=lat, lng=lng, dist=dist, lat_lag = 0.8)

    # Data preprocessing
    buildings = data_preprocessing.data_preprocessing(raw_buildings)

    buildings = pybdshadow.bd_preprocess(buildings)

    #Given UTC time
    date = pd.to_datetime('2022-01-01 12:45:33.959797119')\
        .tz_localize('US/Eastern')\
        .tz_convert('UTC')
    #Calculate shadows
    shadows = pybdshadow.bdshadow_sunlight(buildings,date,roof=True,include_building = False)

    fig = plt.figure(1, (12, 12))
    ax = plt.subplot(111)

    # plot buildings
    buildings.plot(ax=ax)

    # plot shadows
    shadows.plot(ax=ax, alpha=0.7,
                column='type',
                categorical=True,
                cmap='Set1_r',
                legend=True)

    # 3D visualization Visualize using keplergl
    pybdshadow.show_bdshadow(buildings = buildings,shadows = shadows)
