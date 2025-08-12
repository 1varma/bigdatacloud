# %%
import pymysql, csv, time

conn = pymysql.connect(host="mysql.clarksonmsda.org", port=3306, user="juttua", passwd="Muralikrishna9", db="juttua_wifi", autocommit=True)

curr = conn.cursor()

# %%
with open('nov_23_nyc_flights.csv','r', encoding='latin-1') as f:
    data_flights = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

with open('airlines.csv','r', encoding='latin-1') as f:
    data_airlines = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

# %%
from datetime import datetime

for values in data_flights:
    values['UnixTime'] = datetime.fromtimestamp(int(float(values['UnixTime']))).strftime('%Y-%m-%d %H:%M:%S')

# %%
curr.execute("DROP TABLE IF EXISTS juttua_datapoints")
curr.execute("DROP TABLE IF EXISTS juttua_flights")
curr.execute("DROP TABLE IF EXISTS juttua_airlines")



curr.execute(
    '''
    CREATE TABLE juttua_airlines(
        aid INT auto_increment PRIMARY KEY,
        airline VARCHAR(255),
        callsign VARCHAR(255),
        country VARCHAR(255),
        icao VARCHAR(3) unique
    )
''')

curr.execute(
    '''
    CREATE TABLE juttua_flights(
        fid INT auto_increment PRIMARY KEY,
        full_code VARCHAR(10) UNIQUE,
        aid INT,
        FOREIGN KEY (aid) REFERENCES juttua_airlines(aid)
    )
''')

curr.execute(
    '''
    CREATE TABLE juttua_datapoints(
        dpid INT AUTO_INCREMENT PRIMARY KEY,
        date_time datetime,
        hex varchar(12),
        squawk int,
        fid int,
        lat decimal(9,6),
        lon decimal(9, 6),
        gs decimal(6,2),
        alt_gps int,
        alt_baro int,
        cat varchar(3),
        track decimal(6,2),
        nav_heading decimal(6,2),
        foreign key (fid) references juttua_flights(fid)
    )
''')

# %%
def batch_insert(query, data, batch_size=1000):
    for i in range(0, len(data), batch_size):
        try:
            curr.executemany(query, data[i:i+batch_size])
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()

# %%
airline_data = set()
for row in data_airlines:
    if row['Active'] == 'Y':
        airline_data.add((row['ICAO'], row['Name'], row['Callsign'], row['Country']))

# %%
batch_insert(
    '''Insert Ignore into juttua_airlines (icao, airline, callsign, country) values (%s, %s, %s, %s)''',
    list(airline_data)
)

# %%
data_flight = set()

for row in data_flights:
    data_flight.add((row['flight Num  '], row['flight Num  '][:3]))

batch_insert(
    '''Insert Ignore into juttua_flights (full_code, aid)
    (Select %s, a.aid from juttua_airlines as a where a.icao = %s)''',
    list(data_flight)
)

# %%
data_datapoint = set()

for row in data_flights:
    data_datapoint.add((row['UnixTime'], row['Hex ID'], row['Squawk'], row['Lat'], row['Lon'], row['GroundSpeed'], row['GPS Altitude'], row['Pressure Altitude'], row['Category'], row['track'], row['nav_heading'], row['flight Num  ']))


# %%
batch_insert(
    '''Insert Ignore into juttua_datapoints (date_time, hex, squawk, fid, lat, lon, gs, alt_gps, alt_baro, cat, track, nav_heading)
    (Select %s, %s, %s, f.fid, %s, %s, %s, %s, %s, %s, %s, %s from juttua_flights as f where f.full_code = %s)''',
    list(data_datapoint),
    10000
)

# %%
curr.close()
conn.close()


