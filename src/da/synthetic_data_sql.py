from datetime import datetime, timezone
import csv
import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='', database='MSDPM')
cursor = mydb.cursor()

filename ="SyntheticData.csv"
with open(filename, 'r') as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    mySql_insert_query = "INSERT INTO ms_table (ms_id, time, geo, CO, NO2) VALUES (%s, %s, ST_GeomFromText(%s), %s, %s)"
    firstline = True
    for row in csv_data:
        if firstline:    #skip first line
       	    firstline = False
        else:
            ms_id=row[0]
            time=row[1]
            lon=row[2]
            lat=row[3]
            no2=row[4]
			co=row[5]
            coord = str("POINT(") + str(round(float(lat),6)) + ' ' + str(round(float(lon),6)) + str(")")
            records_to_insert = [(ms_id, time, coord, co, no2)]
            cursor.executemany(mySql_insert_query, records_to_insert)

#close the connection to the database.
cursor.close()
print ("Done")