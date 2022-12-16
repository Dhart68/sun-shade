from suncalc import get_times
def sunlight_hour():
    times = get_times(date, lon, lat)
    date_sunrise = times['sunrise']
    data_sunset = times['sunset']
    timestamp_sunrise = pd.Series(date_sunrise).astype('int')
    timestamp_sunset = pd.Series(data_sunset).astype('int')
    sunlighthour = (
        timestamp_sunset.iloc[0]-timestamp_sunrise.iloc[0])/(1000000000*3600)
    return sunlighthour
