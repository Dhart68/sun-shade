import requests
import pandas as pd

url='https://power.larc.nasa.gov/api/temporal/daily/point'

def historical_solar_radiation(lat, lon, start_date,end_date):
    '''Return a day-by-day historical solar radiation for one year at a certain place, given its latitude and longitude.'''
    params= {
        'parameters':'ALLSKY_SFC_SW_DWN','community':'RE', 'latitude': lat,
<<<<<<< HEAD
             'longitude': lon, 'start':'20210101','end':'20220101','format':'JSON'
=======
             'longitude': lon, 'start':start_date,'end':end_date,'format':'JSON'
>>>>>>> e89abecfe8bdb276f916efef6c8fd03fb5bc037b
    }
    solar_radiation = requests.get(url, params=params).json()['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    df=pd.DataFrame([solar_radiation]).T.rename(columns={0:'radiation'})
    return df

if __name__ == '__main__':
    #historical_solar_radiation(lat, lon, start_date,end_date)
    print(historical_solar_radiation(51.5072, 0.1276, 20210101,20210331))
