INFO DATA ACQUISITION

Python libraries: (installing with the command: pip install 'libraryname')

urllib.request

json 

ssl 

datetime: datetime, timezone, timedelta 

mysql.connector 

pytz 

netCDF4 import Dataset 

aqi 

os 

cdsapi 

csv 


The above list has the number of libraries needed to be installed before running the Python script. Next, I am going to explain the use of each one: 

The urllib.request module defines functions and classes which help in opening URLs (mostly HTTP) in a complex world — basic and digest authentication, redirections, cookies and more. 

It is used to connect to aqicn.org via https to request every base station data. 

Python has a built-in package called json, which can be used to work with JavaScript object notation (JSON) data. 

All base station data provided by aqicn is given in a json format. 

The ssl module provides access to Transport Layer Security (often known as “Secure Sockets Layer”) encryption and peer authentication facilities for network sockets, both client-side and server-side. 

It is a complementary module for urllib.request to be able to connect to aqicn website. 

The datetime module supplies classes for manipulating dates and times.  

Submodules as datetime, timedelta and timezone are used in base station script and datetime and timedelta submodule in SAT script. 

Submodule datetime is used to create a timestamp for each data. On the other hand, timezone is used to transform all time information to UTC in order to have all referenced equally. 

The pytz library allows accurate and cross platform time zone calculations using Python. It solves the issue of ambiguous times at the end of daylight-saving time, and time zones. It is complementing datetime module. 

The mysql.connector module is used to connect to a MySQL database. In both scripts, SAT and Base Station is needed to upload all data requested. We can also manage the databases directly from Python. 

The library netCDF4 is a Python interface to the netCDF C library. It is used to manage the data provided from satellites format. The sub module Dataset is a collection of dimensions, groups, variables and attributes. Together they describe the meaning of data and relations among data fields stored in a netCDF file. 

The aqi library is used to convert the values from aqicn database which based on AQI US EPA to concentration ug/m3. Please install this library with the following command: pip install git+https://github.com/hrbonz/python-aqi.git

Python has a built-in package called os, which can be used to delete files. It is used to delete old satellite files from satellite. 

The cdsapi is a service providing programmatic access to ADS data. It is used to access and download to CAMS database. For using that, first copy the code displayed called .cdsapirc, in the path $HOME/.cdsapirc 

The csv library will help to trasform mobile data .csv file to mysql database format

· tables_creation.py 

The aim of this script is to create the database and all the necessary tables for the data acquisition. On the definition of mydb parameter, you would be replenishing the attributes with the values that corresponds to your MySQL server, like host, user, password, port, etc. 

 

· bs_fixed.py 

The aim of this script is to generate a database table of all the Base Stations we require values for our system, in the specific area. It will request for the API the name and geolocations of all the Base Stations, that they will contain a unique identifier for everyone. 

 
· bs_values.py 

The aim of this script is to upload all pollution data from base station to the server database table in an orderly manner. The data is stored on the table where each row has the timestamp when data was taken and the value of all of the pollutants each base station has measured. 

Base station can measure up to these pollutants: CO, NO2, SO2, O3, PM2.5, PM10. 

All this data is taken from aqicn website, where the most part of base stations of the world are stored and uploaded hourly. Using a list where all base station we want to analyse are written; with a HTTPS request loop we get a JSON of the base station one by one.  

From these JSON we extract the information and converting it to pollutants values in ug/m^3 ant the time to UTC format, in order to have all base station synchronized. 

We upload all this amount of data to MySQL database using a query with the correct order of all data. 

Once all data is extracted, the connection with database is closed and data stored in database table from 24h before is removed from the database. 

 

· sat_request.py 

Retrieve data from CAMS API by a retrieve function, selecting the specs like pollutants, time, level above the surface and area that requires our system. 

CAMS provide us the pollutant data of CO, NO2, SO2, O3, PM2.5 and PM10 of the whole continent of the Iberian Peninsula in a netCDF file. 

 
· sat_sql.py 

The aim of this script is to convert all data from satellites provided by CAMS to organized tables. These tables have the value of each pollutant, acquisition time and the position in a pointer with a longitude and latitude. 

<<<<<<< HEAD
Extracting data from netCDF file obtained in sat_request script, it uploads all data to an already created table in MySQL database using queries.  Once all data is extracted, the connection with database is closed and the netCDF file from 48h before is removed from the server. Also is remove the 2 days before old data from de database table. 
=======
Extracting data from netCDF file obtained in sat_request script, it uploads all data to an already created table in MySQL database using queries.  Once all data is extracted, the connection with database is closed and the netCDF file from 48h before is removed from the server. Also is remove the 2 days before old data from de database table.

 
· synthetic_data_sql.py 
This script transforms the syntethic data (that simulate mobile sensors movement) in .csv format to database format and import to the correspondig table.

 
>>>>>>> 42b3d8c... Updated code to treat synthetic data
