# InfluxDB
https://docs.influxdata.com/influxdb/v1.7/

## Start Influx

```
influx
```


## DB

```
create database <name of database>
use <name of dabtabase>
```

## Measurements


### Insert 

별도로 table을 생성하거나 할 필요 없이  
insert 하면 생성과 추가를 같이 함

```
insert <name of Measurements> [tag=value ...]
ex) insert temperature where="home",degree=34.4
```

### delete Measurement

```
drop measurement <name of measurement>
```

### delete field

*note* delete는 time 으로만 가능.  
delete 를 하는 환경을 전제하지 않음.  
데이터 관리는  
1. Down Sampling
2. Retention Policy
로 필요없는 데이터의 관리를 해야한다. 

```
delete from <name of measurement> where time=<time of target>
```

+ 확인

```
show <name of Measurements>
```

## Precision

```
precision rfc3339
```
2019-05-12T09:38:41.3493649787 꼴로 출력


## USER

```
create user <username> with password '<password>' with all privileges

## else

+ SQL 쿼리 사용해서 조회
+ timestamp가 같다면 overwirte함. timestamp가 같다면 중복되는 데이터가 존재하지는 않을듯.


