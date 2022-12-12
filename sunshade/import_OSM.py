def import_OSM(lat=40.775, lng=-73.96, dist=50, lat_lag = 0.8):
    # import data from OSM
    tags = {"building": True, 'height': True, 'ele': True}
    #center_point = (lat, lng)
    #raw_buildings = ox.geometries_from_point(center_point, tags=tags, dist=dist)
    # select only buildings south of the center point (1 degree lat = 111 111 m) with a lag of lat_lag
    if lat>0:
        optimized_point = (lat-(round(dist/111111,4)*lat_lag), lng)
    else:
        optimized_point = (lat+(round(dist/111111,4)*lat_lag), lng)
        
    raw_buildings = ox.geometries_from_point(optimized_point, tags=tags, dist=dist)
    
    return raw_buildings
