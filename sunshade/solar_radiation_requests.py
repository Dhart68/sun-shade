import requests
import pandas as pd

url='https://power.larc.nasa.gov/api/temporal/daily/point'

def historical_solar_radiation(lat, lon):
    '''Return a day-by-day historical solar radiation for one year at a certain place, given its latitude and longitude.'''
    params= {
        'parameters':'ALLSKY_SFC_SW_DWN','community':'RE', 'latitude': lat,
             'longitude': lon, 'start':'20210101','end':'20220101','format':'JSON'
    }
    solar_radiation = requests.get(url, params=params).json()['properties']['parameter']['ALLSKY_SFC_SW_DWN']
    df=pd.DataFrame([solar_radiation]).T.rename(columns={0:'radiation'})

    df.reset_index(inplace=True)
    df['date'] = df['index'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))

    return df

if __name__ == '__main__':
    #historical_solar_radiation(lat, lon)
    print(historical_solar_radiation(51.5072, 0.1276))
