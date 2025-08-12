#The following code reads csv data from test.csv into memory as a list of #dictionaries called ‘data’ . Example:
#[{'col2': 2, 'col3': 3, 'col1': 1}, {'col2': 5, 'col3': 6, 'col1': 4}]
import csv
with open('wifi_2023.csv','r', encoding='latin-1') as f:
    data = [{k: str(v) for k, v in row.items()}
        for row in csv.DictReader(f, skipinitialspace=True)]

manufacturerCounts = {}

for row in data:
    if "CPH" in row['SSID']:
        mac = row['MAC']
        oui = ":".join(mac.split(":")[:3])

        if oui in manufacturerCounts:
            manufacturerCounts[oui] += 1
        
        else:
            manufacturerCounts[oui] = 1



print("mac manufacturer | count")
print("---------------- | -------------")
for oui, count in sorted(manufacturerCounts.items()):
    print(f"{oui}         |      {count}")


channelCount = {}

channelMac = {}

for row in data:

    if row['Type'] == 'WIFI':
        channel = row['Channel']
        mac = row['MAC']
    
        if channel not in channelMac:
            channelMac[channel] = set()
            channelCount[channel] = 0
        
        if mac not in channelMac[channel]:
            channelMac[channel].add(mac)
            channelCount[channel] += 1

print("Channel | count")
print("------- | ------")
for channel in sorted(channelCount.keys(), key=int):
    print(f"{channel} | {channelCount[channel]}")

lat_max = 44.6687863
lon_min = -74.9873144
lat_min = 44.668504
lon_max = -74.986579

deviceDates = {}

for row in data:
    
    if row['Type'] in ['BLE', 'BT']:
        lat = float(row['CurrentLatitude'])
        lon = float(row['CurrentLongitude'])

        if (lat_min <= lat <= lat_max) and (lon_min <= lon <= lon_max):
            mac = row['MAC']

            date = row['FirstSeen'].split()[0]

            if mac not in deviceDates:
                deviceDates[mac] = set()
            
            deviceDates[mac].add(date)

frequencyDevices = []

for mac, dates in deviceDates.items():
    if len(dates) >= 4:
        frequencyDevices.append((mac, len(dates)))

frequencyDevices.sort(key = lambda x: x[1], reverse=True)

print("MAC Address | Number of Days Seen")
print("----------- | -------------------")
for mac, days in frequencyDevices:
    print(f"{mac} | {days}")