import json
import requests
from requests.auth import HTTPBasicAuth

headers = {'apiKey': '375da54c-885f-4080-99c2-cec73d237a4f', 'Accept': 'application/json'}
response = requests.get('https://api.building-density.haastech.org/api/scenarios/bb87c943-85e2-4e7c-92d9-364fb52b2b11/currentOccupancyStatistics', headers = headers)

response_dict = response.json()
for library_info in response_dict["results"]["data"]:
    print(library_info["name"] + ": " + str(library_info["clientCount"]))
