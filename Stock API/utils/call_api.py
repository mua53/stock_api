#Get Data from api in internet
import requests
import wget

#get data
def call_get(url, header):
    request = requests.request("GET", url, headers= header)
    return request.json()

def call_post(url, header, payload):
    request = requests.request("POST", url, headers= header, data=payload)
    return request.json()

def call_download(url, name_file):
    response = wget.download(url, name_file)
    return response
