from datetime import datetime, timedelta
import cdsapi

c = cdsapi.Client()
today=datetime.today().strftime("%Y-%m-%d")

c.retrieve(
    'cams-europe-air-quality-forecasts',
    {
        'variable': [
            'carbon_monoxide', 'nitrogen_dioxide', 'sulphur_dioxide',
            'ozone', 'particulate_matter_10um', 'particulate_matter_2.5um',
        ],
        'model': 'ensemble',
        'level': '0',
        'date': today+'/'+today,
        'type': 'forecast',
        'time': '00:00',
        'leadtime_hour': [
            '0', '1', '2',
            '3', '4', '5',
            '6', '7', '8',
            '9', '10', '11',
            '12', '13', '14',
            '15', '16', '17',
            '18', '19', '20',
            '21', '22', '23',
        ],
        'area': [
            43.93, -9.82, 35.9,
            4.63,
        ],
        'format': 'netcdf',
    },
    'SAT_'+today+'.nc')