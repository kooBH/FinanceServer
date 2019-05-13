
# InfluxDB with Python

```python
pip install influxdb
```

## 예제 코드 

```python
from influxdb import InfluxDBClient
from datetime import datetime

timestamp = datetime.utcnow() # <-- get time in UTC
timestamp =  timestamp.isoformat("T") + "Z" # Zulu timezone

host='localhost'
port=8086

user='kbh'
pw='qwer1234'

dbname= 'test_db'
dbuser= 'test_user'
dbpass= 'qwer1234'

query = 'select * from test_m'

val = 1.1

body = [
    {
        "measurement":"test_m",
        "time":timestamp,
        "fields":{
            'value':val
       }
    }        
]

# client = InfluxDBClient(host, port, user, password, dbname)
client = InfluxDBClient(host, port, user, pw, dbname)

print("Create database: " + dbname)
client.create_database(dbname)

print("Create a retention policy")
client.create_retention_policy('awesome_policy', '3d', 3, default=True)

print("Switch user: " + dbuser)
client.switch_user(dbuser, dbpass)

print("Write points: {0}".format(body))
client.write_points(body)

print("Querying data: " + query)
result = client.query(query)

print("Result: {0}".format(result))

print("Switch user: " + user)
client.switch_user(user, pw)

print("Drop database: " + dbname)
client.drop_database(dbname)
```
