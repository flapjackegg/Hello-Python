import requests


def create_server(name, host):
    URL = 'http://127.0.0.1:5000/servers/'
    name = name.strip()
    host = host.strip()
    data = {'name': name, 'host': host}
    resp = requests.post(URL, json=data)
    return resp.json()
