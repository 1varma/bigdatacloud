# %%
import requests, json, datetime, csv

# %%
url = f'http://api.openweathermap.org/data/2.5/weather?zip=54590,us&appid=a6962678a5cba51e8db12b46bc87a867'
r = requests.get(url)
data = json.loads(r.text)
print(data)

# %%
def getDayLight(zip):
    url = f'http://api.openweathermap.org/data/2.5/weather?zip={zip},us&appid=a6962678a5cba51e8db12b46bc87a867'
    r = requests.get(url)
    data = json.loads(r.text)

    res = {}

    status = 'Ok' if data['cod'] == 200 else 'Error' if data['cod'] == 400 else 'None'

    if status != 'Ok':
        res['status'] = status
        return res
    
    rise = datetime.datetime.fromtimestamp(int(data['sys']['sunrise']))
    rise = datetime.datetime.fromtimestamp(int(data['sys']['sunset']))


    res['status'] = status
    res['rise'] = rise.strftime("%H:%M:%S")
    res['set'] = rise.strftime("%H:%M:%S")
    res['riseunix'] = data['sys']['sunrise']
    res['setunix'] = data['sys']['sunset']

    return res

# %%
print(getDayLight(54590))

# %%
inputfile = 'ziplist.csv'


with open(inputfile, mode='r', newline='') as infile:
    csvreader = csv.reader(infile)
    header = next(csvreader)
    rows = [header]

    for row in csvreader:
        zipcode = row[0]
        daylight = getDayLight(zipcode)

        if daylight.get('status') == 'Ok':
            row[1] = daylight['rise']
            row[2] = daylight['set']
        else:
            row[1] = None
            row[2] = None
        rows.append(row)

with open(inputfile, mode='w', newline='') as outfile:
    csvwriter = csv.writer(outfile)
    csvwriter.writerows(rows)


