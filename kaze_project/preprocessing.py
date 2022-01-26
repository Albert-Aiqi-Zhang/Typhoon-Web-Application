import numpy as np
import pandas as pd
from datetime import datetime
from pandas.io import sql
import pymysql
import csv
import os
import sys
import pymysql

df1 = pd.read_csv("../database_engineering/data_of_typhoon/table2001.csv", encoding="SHIFT-JIS")
f = lambda x: datetime(x["年"], x["月"], x["日"], x["時（UTC）"], 0, 0)
df1["datetime"] = df1.apply(f, axis=1)
df1.drop(columns=["年", "月", "日", "時（UTC）"], inplace=True)
df1_new = df1.iloc[:,[14,0,1,2,3,4,5,6,7,8,9,10,11,12,13]]

df1_new.columns = ["datetime", "typhoon_number", "typhoon_name", "class", "latitude", "longitude", "center_pressure",
                  "max_velocity", "50KT_major_direction", "50KT_major", "50KT_minor",
                   "30KT_major_direction", "30KT_major", "30KT_minor", "landing"]
df1_new.to_csv("../database_engineering/data_after/table2001.csv")
f = lambda x: datetime(x["年"], x["月"], x["日"], x["時（UTC）"], 0, 0)

for i in range(2, 19):
    if i < 10:
        r = "0" + str(i)
    else:
        r = str(i)
    df = pd.read_csv("../database_engineering/data_of_typhoon/table20" + r + ".csv", encoding="SHIFT-JIS")
    df["datetime"] = df.apply(f, axis=1)
    df.drop(columns=["年", "月", "日", "時（UTC）"], inplace=True)
    df_new = df.iloc[:,[14,0,1,2,3,4,5,6,7,8,9,10,11,12,13]]
    df_new.columns = ["datetime", "typhoon_number", "typhoon_name", "class", "latitude", "longitude", "center_pressure",
                  "max_velocity", "50KT_major_direction", "50KT_major", "50KT_minor",
                   "30KT_major_direction", "30KT_major", "30KT_minor", "landing"]
    df_new.to_csv("../database_engineering/data_after/table20" + r + ".csv")

pymysql.install_as_MySQLdb()
data = pd.read_csv("../database_engineering/data_after/table2001.csv")
db = MySQLdb.connect(host = "localhost", user = "root",
                          passwd = "12345678", db = "kaze", charset = "utf8")
conn = MySQLdb.Connection(host = 'localhost',user = 'root',password = '12345678',port = 3306,
                          database = 'kaze')
#sql.to_sql(data, 'train', db)
#db.close()

cur = pymysql.cursors.Cursor(connection = conn)
cur.execute("""
create table tbl01(
id int auto_increment primary key,
dtime datetime,
typhoon_number int,
typhoon_name varchar(256),
class int,
latitude float,
longitude float,
center_pressure int,
max_velocity int,
50KT_major_direction int,
50KT_major int,
50KT_minor int,
30KT_major_direction int,
30KT_major int,
30KT_minor int,
landing int)""")

conn.commit()

data = pd.read_csv('../database_engineering/data_after/table2001.csv')
data = data.astype(str).iloc[:, 1:].values.tolist()
cur.executemany("insert into tbl01 values(null, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
conn.commit()

local_dir=r'../database_engineering/data_after/table2001.csv'
csv_reader(local_dir)

for i in range(2, 19):
    if i < 10:
        r = "0" + str(i)
    else:
        r = str(i)
    cur = pymysql.cursors.Cursor(connection = conn)
    cur.execute("""
    create table tbl""" + r + """(
    id int auto_increment primary key,
    dtime datetime,
    typhoon_number int,
    typhoon_name varchar(256),
    class int,
    latitude float,
    longitude float,
    center_pressure int,
    max_velocity int,
    50KT_major_direction int,
    50KT_major int,
    50KT_minor int,
    30KT_major_direction int,
    30KT_major int,
    30KT_minor int,
    landing int)""")

    conn.commit()

    data = pd.read_csv("../database_engineering/data_after/table20" + r + ".csv")
    data = data.astype(str).iloc[:, 1:].values.tolist()
    
    cur.executemany("insert into tbl" + r + " values(null, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", data)
    conn.commit()