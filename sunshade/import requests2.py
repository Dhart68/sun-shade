import requests
import pandas as pd

url='https://power.larc.nasa.gov/api/temporal/monthly/point'

def historical_solar_radiation(lat, lon):
    '''Return a day-by-day historical solar radiation for one year at a certain place, given its latitude and longitude.'''
    params= {
        'parameters':'ALLSKY_SFC_SW_DWN','community':'RE', 'longitude': lon,'latitude': lat,
            'start':'2021','end':'2021','format':'JSON'
    }
    solar_radiation = requests.get(url, params=params).json()['properties']['parameter']['ALLSKY_SFC_SW_DWN']['202113']
    print(f"Annual estimation of solar radiation for this place is: {solar_radiation} Kw/h/m^2/day")
    if solar_radiation>=4:
        print('This place could provide the minimum required solar energy to generate electricity')
    else:
        print('This place is not recommended to install a solar panel')

if __name__ == '__main__':
    print(historical_solar_radiation(60.4720, 8.4676))
