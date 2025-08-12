file = open('access_subset.log', 'r')
text = file.read()

lines = text.split('\n')

parsedData = []

#here httpErrors has error code in general 200 is used for success, 301 is redirects, 400 is bad connect, 404 is not found, 405 is method not move, etc.,
httpErrors = ["200", "301", "302", "304", "400", "404", "405", "499"]

for line in lines:
    line = line.split()
    IP = line[0]
    dayArray, hour, minute, second = line[3].strip("[").split(":")
    dayArray = dayArray.split("/")
    day, month, year = dayArray
    UTC_offset = line[4].strip("]")
    httpErrorCode = next((line[i] for i in range(len(line)) if line[i] in httpErrors), "")
    parsedData.append([IP, year, month, day, hour, minute, second, UTC_offset, httpErrorCode])
    #print(httpErrorCode)


for line in parsedData:
    print(line)