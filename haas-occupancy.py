import json
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class BuildingOccupancy:
    currentBuildings = {
        "70e3755b-718d-42d0-b285-345f5e488b74": "Doe Library",
    }
    buildings = {
        "70e3755b-718d-42d0-b285-345f5e488b74": "Doe Library",
        "f7f78915-550d-4691-b762-1a75cc807c09": "Bancroft Library",
        "843370d6-008c-4d5f-8be1-7653a9e1f036": "Hargrove Music Library",
        "31a41038-11fb-46c1-a64e-f1e83961d622": "Doe-Gardner Stacks"
    }

    def __init__(self, id, count):
        self.id = id
        self.name = self.buildings[id]
        self.count = count

    def __str__(self):
        return self.name + ": " + str(self.count)


def updateFb(id, count):
    supported = BuildingOccupancy.currentBuildings
    if id in supported.keys():
        doc_ref = db.collection('Occupancy').document(
            BuildingOccupancy.currentBuildings[id])
        doc_ref.set({
            'live': count,
        })


# initialize firebase app
cred = credentials.Certificate(
    "./haas-occupancy-test-firebase-adminsdk-371zh-527e51ccfc.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# grab data from haas server
headers = {'apiKey': '375da54c-885f-4080-99c2-cec73d237a4f',
           'Accept': 'application/json'}
response = requests.get(
    'https://api.building-density.haastech.org/api/scenarios/bb87c943-85e2-4e7c-92d9-364fb52b2b11/currentOccupancyStatistics', headers=headers)
response_dict = response.json()
snapshot = []
for library_info in response_dict["results"]["data"]:
    id = library_info['id']
    clientCount = library_info['clientCount']
    buildingOccupancy = BuildingOccupancy(id, clientCount)
    snapshot.append(buildingOccupancy)

# process building occupancy data
for building in snapshot:
    updateFb(building.id, building.count)
