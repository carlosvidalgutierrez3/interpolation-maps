import mysql.connector

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  passwd='',
  port=''
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE MSDPM")

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  passwd='',
  port='',
  database='MSDPM'
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE sat_table (time DATETIME,geo_sat POINT,CO DECIMAL(9,6),NO2 DECIMAL(9,6),SO2 DECIMAL(9,6),O3 DECIMAL(9,6),PM10 DECIMAL(9,6),PM25 DECIMAL(9,6))")
mycursor.execute("CREATE TABLE bs_fixed (bs_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,bs_name VARCHAR(255),geo_bs POINT)")
mycursor.execute("CREATE TABLE bs_values (bs_id INT,FOREIGN KEY(bs_id) REFERENCES bs_fixed(bs_id),time DATETIME,CO DECIMAL(6,2) DEFAULT NULL,NO2 DECIMAL(6,2) DEFAULT NULL,SO2 DECIMAL(6,2) DEFAULT NULL,O3 DECIMAL(6,2) DEFAULT NULL,PM10 DECIMAL(6,2) DEFAULT NULL,PM25 DECIMAL(6,2) DEFAULT NULL)")

mycursor.execute("CREATE TABLE layer_ext (time DATETIME,geo POINT,CO DECIMAL(6,2),NO2 DECIMAL(6,2),SO2 DECIMAL(6,2),O3 DECIMAL(6,2),PM10 DECIMAL(6,2),PM25 DECIMAL(6,2))")
mycursor.execute("CREATE TABLE layer_mid (time DATETIME,geo POINT,city BOOLEAN DEFAULT 0,CO DECIMAL(6,2),NO2 DECIMAL(6,2),SO2 DECIMAL(6,2),O3 DECIMAL(6,2),PM10 DECIMAL(6,2),PM25 DECIMAL(6,2))")
mycursor.execute("CREATE TABLE layer_int (time DATETIME,geo POINT,CO DECIMAL(6,2),NO2 DECIMAL(6,2),SO2 DECIMAL(6,2),O3 DECIMAL(6,2),PM10 DECIMAL(6,2),PM25 DECIMAL(6,2))")
