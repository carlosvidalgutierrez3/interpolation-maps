import urllib.request
import json
import ssl
from datetime import datetime, timezone
import mysql.connector


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

mySql_insert_query = """INSERT INTO bs_fixed (bs_name, geo_bs) VALUES (%s, ST_GeomFromText(%s))"""

i = 0
while i < len(list):

    url = list[i].rstrip('\n') + '?token=' + token
    request = urllib.request.urlopen(url, context=ctx).read()

    data = json.loads(request).get('data')
    status = json.loads(request).get('status')

    if status == 'ok':
        city = data.get('city')
        if city != None:
            if city.get('geo') != None:
                lat = city.get('geo')[0]
                lon = city.get('geo')[1]
            city = city.get('name')
            coord = str("POINT(") + str(round(lat,4)) + ' ' + str(round(lon,4)) + str(")")

        records_to_insert = [(city, coord)]
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        
        i += 1
        print(i)

if (connection.is_connected()):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
