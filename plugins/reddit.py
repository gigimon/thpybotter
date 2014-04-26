import requests

def parse(url):
    if url[-1:] == "/":
        url = url[:-1]

    if url[-5:] != ".json":
        url += ".json"

    json_api = requests.get(url).json()

    if len(filter(None, url.split("/"))) >= 8:
        # This is a comment
        return json_api[1]['data']['children'][0]['data']
    else:
        # This is a thread
        return json_api[0]['data']['children'][0]['data']
