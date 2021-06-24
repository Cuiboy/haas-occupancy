import json
import requests
from requests.auth import HTTPBasicAuth
import pygsheets
import pandas as pd
import numpy as np
from datetime import datetime


def writeDataTest(col):
    gc = pygsheets.authorize(service_file ='/Users/cuiboy/Desktop/Code/Berkeley/OCTO/haas-occupancy/haas-wifi-occupancy-3a6c045f1b95.json')
    df = pd.DataFrame()
    df[str(datetime.now())] = col
    sh = gc.open('Occupancy Data Test')
    wks = sh[0]
    targetCol = 0
    curVal = wks.get_all_values()
    curValArr = np.array(curVal).transpose()
    for i, e in enumerate(curValArr):
        r = any(x for x in e)
        if r is False:
            targetCol = i + 1
            break
    wks.set_dataframe(df,(1, targetCol))

headers = {'apiKey': '375da54c-885f-4080-99c2-cec73d237a4f', 'Accept': 'application/json'}
response = requests.get('https://api.building-density.haastech.org/api/scenarios/bb87c943-85e2-4e7c-92d9-364fb52b2b11/currentOccupancyStatistics', headers = headers)
response_dict = response.json()
snapshot = []
for library_info in response_dict["results"]["data"]:
    snapshot.append(library_info["clientCount"])
writeDataTest(snapshot)
