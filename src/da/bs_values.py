import urllib.request
import json
import ssl
from datetime import datetime, timezone, timedelta
import mysql.connector
import pytz
import aqi


connection = mysql.connector.connect(host='localhost', port='8889', user='root', password='root', database='MSDPM')

if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)


list = open("BSlist_Test.txt", "r").readlines()
token = 'f095e89075b4cb0f1e0b0aaf3a3ce75d664993bd'
ctx = ssl._create_unverified_context()

mySql_insert_query = """INSERT INTO bs_values (bs_id, time, CO, NO2, SO2, O3, PM10, PM25) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """

i = 0
while i < len(list):
    
    url = list[i].rstrip('\n') + '?token=' + token
    request = urllib.request.urlopen(url, context=ctx).read()

    print(url)

    data = json.loads(request).get('data')
    status = json.loads(request).get('status')

    if status == 'ok':
        bs_id=0
        city = data.get('city')
        if city != None:
            if city.get('geo') != None:
                lat = city.get('geo')[0]
                lon = city.get('geo')[1]
                city = city.get('name')
                sql='SELECT bs_id FROM bs_fixed WHERE ST_X(geo_bs)='+str(round(lat,4))+' AND ST_Y(geo_bs)='+str(round(lon,4))
                cursor.execute(sql)
                rows=cursor.fetchall()
                bs_id=rows[0][0]
            time = data.get('time').get('s')
        if time != "":
            timezn = data.get('time').get('tz')
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            if int(timezn[:-3]) > 0:
                tz = pytz.timezone('Etc/GMT-'+str(int(timezn[:-3])))
            else:
                tz = pytz.timezone('Etc/GMT+'+str(-int(timezn[:-3])))
            date = tz.normalize(tz.localize(dt)).astimezone(pytz.utc)

        if data.get('iaqi') != [] and data.get('iaqi') != None:
            co = data.get('iaqi').get('co')
            if co != None:
                co = co.get('v')
                co = float(aqi.to_cc(aqi.POLLUTANT_CO_8H, co, algo=aqi.ALGO_EPA))*1145
            no2 = data.get('iaqi').get('no2')
            if no2 != None:
                no2 = no2.get('v')
                no2 = float(aqi.to_cc(aqi.POLLUTANT_NO2_1H, no2, algo=aqi.ALGO_EPA))*1.88
            so2 = data.get('iaqi').get('so2')
            if so2 != None:
                so2 = so2.get('v')
                so2 = float(aqi.to_cc(aqi.POLLUTANT_SO2_1H, so2, algo=aqi.ALGO_EPA))*2.62
            o3 = data.get('iaqi').get('o3')
            if o3 != None:
                o3 = o3.get('v')
                o3 = float(aqi.to_cc(aqi.POLLUTANT_O3_8H, o3, algo=aqi.ALGO_EPA))*2000
            pm10 = data.get('iaqi').get('pm10')
            if pm10 != None:
                pm10 = pm10.get('v')
                pm10 = float(aqi.to_cc(aqi.POLLUTANT_PM10, pm10, algo=aqi.ALGO_EPA))
            pm25 = data.get('iaqi').get('pm25')
            if pm25 != None:
                pm25 = pm25.get('v')
                pm25 = float(aqi.to_cc(aqi.POLLUTANT_PM25, pm25, algo=aqi.ALGO_EPA))
        
        records_to_insert = [(bs_id, date, co, no2, so2, o3, pm10, pm25)]
        
        date = datetime.now(tz=timezone.utc);
        
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        
        i += 1
        print(i)

cursor = connection.cursor()
delete=(datetime.utcnow()- timedelta(days=7)).strftime("%Y-%m-%d %H:00:00")
sql = "DELETE FROM bs_values WHERE time = %s"
adr = (delete, )
cursor.execute(sql, adr)
connection.commit()


if (connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
