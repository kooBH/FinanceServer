from influxdb import InfluxDBClient
from datetime import datetime

import secret

timestamp = datetime(2018, 8, 30, 1, 26, 55, 731039) 
timestamp =  timestamp.isoformat("T") + "Z" # Zulu timezone

host=secret.host
port=secret.port

user=secret.user
pw=secret.pw

dbname= 'test_db'
dbuser= 'test_user'
dbpass= 'qwer1234'

query = 'select * from test_m'

val = 1.3

body = [
    {
        "measurement":"test_m",
        "time":timestamp,
        "fields":{
            'value':val
       }
    }        
]


client = InfluxDBClient(host, port, user, pw, dbname)

client.write_points(body)
