#Get Data from api in internet
import requests
import json

#get data
def call_get(url, header):
    request = requests.request("GET", url, headers= header)
    return request.json()

def call_post(url, header, payload):
    request = requests.request("POST", url, headers= header, data=payload)
    return request.json()

