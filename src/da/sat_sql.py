from datetime import datetime, timezone, timedelta
import mysql.connector
from netCDF4 import Dataset
import os

print ("Hello World!\n")

connection = mysql.connector.connect(host='localhost', database='MSDPM', user='root', password='')
if connection.is_connected():
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    cursor = connection.cursor()
    cursor.execute("select database();")
    record = cursor.fetchone()
    print("You're connected to database: ", record)

date=datetime.today().strftime("%Y-%m-%d")
filename ='SAT_'+date+'.nc'
ncin = Dataset(filename, 'r', format='NETCDF4')

time = ncin.variables['time']
lat = ncin.variables['latitude']
lon = ncin.variables['longitude']
level = ncin.variables['level']
co_conc = ncin.variables['co_conc']
no2_conc = ncin.variables['no2_conc']
so2_conc = ncin.variables['so2_conc']
o3_conc = ncin.variables['o3_conc']
pm10_conc = ncin.variables['pm10_conc']
pm2p5_conc = ncin.variables['pm2p5_conc']

mySql_insert_query = "INSERT INTO sat_fixed (time, geo_sat, CO, NO2, SO2, O3, PM10, PM25) VALUES (%s, ST_GeomFromText(%s), %s, %s, %s, %s, %s, %s)"

i = 0
j = 0
k = 0

while k < len(time):
    while i < len(lat):
        while j < len(lon):
            if(lon[j]>180):
                lon_norm=round(lon[j]-360,2)
            else:
                lon_norm=lon[j]
            date_hour=date+' '+str(int(time[k]))+':00:00'
            cursor = connection.cursor()
            
            coord = str("POINT(") + str(lat[i]) + ' ' + str(lon_norm) + str(")")
            records_to_insert = [(date_hour, coord, str(co_conc[k][0][i][j]), str(no2_conc[k][0][i][j]), str(so2_conc[k][0][i][j]), str(o3_conc[k][0][i][j]), str(pm10_conc[k][0][i][j]), str(pm2p5_conc[k][0][i][j]))]
            cursor.executemany(mySql_insert_query, records_to_insert)
            connection.commit()
            j += 1
        print(i)
        j = 0
        i+= 1
    k+=1
    i=0       
     
cursor = connection.cursor()
delete=(datetime.utcnow()- timedelta(days=2)).strftime("%Y-%m-%d")
sql = "DELETE FROM sat_table WHERE time BETWEEN %s AND %s"
adr = (str(delete+' 00:00:00'), str(delete+' 23:00:00'), )
cursor.execute(sql, adr)
connection.commit()

if (connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

delete = (datetime.today()- timedelta(days=7)).strftime("%Y-%m-%d")
if os.path.exists('SAT_'+delete+'.nc'):
  os.remove('SAT_'+delete+'.nc')
  print('The file SAT_'+delete+'.nc has been deleted')
else:
  print('The file SAT_'+delete+'.nc does not exist')
