# Get Data from api in internet
import requests


# get data
def call_get(url, header):
    request = requests.request("GET", url, headers=header)
    return request.json()


def call_post(url, header, payload):
    request = requests.request("POST", url, headers=header, data=payload)
    return request.json()


def call_download(url, name_file):
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with open(name_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)
    return name_file
