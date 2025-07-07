import requests
import time
import pytz
from datetime import datetime, timedelta, timezone

url = "https://yandex.com/time/sync.json?geo=213"
response = requests.get(url)

timestamp: float = response.json()['time']/1000
offset = response.json()['clocks']['213']['offsetString']
print("1)" + response.text)
print("2) Time: " + str(datetime.fromtimestamp(timestamp)) + ", Offset: " + offset)

deltaStart = datetime.now(timezone.utc)
response = requests.get(url)
serverTime = datetime.fromtimestamp(response.json()['time']/1000)
serverTimeUtc = serverTime.astimezone(timezone.utc)
deltaResult = deltaStart - serverTimeUtc

print("3) Delta: " + str(deltaResult))

deltaList = []

for i in range(5):
    deltaStart = datetime.now(timezone.utc)
    response = requests.get(url)

    serverTime = datetime.fromtimestamp(response.json()['time'] / 1000)
    serverTimeUtc = serverTime.astimezone(timezone.utc)
    deltaResult = deltaStart - serverTimeUtc
    deltaList.append(deltaResult)

print("4) Average Delta: " + str(sum(td.total_seconds() for td in deltaList) / 5))