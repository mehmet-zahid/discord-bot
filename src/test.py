import requests

headers = {
    'content-type': "application/json",
    'authorization': "apikey 1G4yBkm7e08TLxKytOkFCW:4NjB6ALxER88zp7JgXk1Wd"
    }

url = "https://api.collectapi.com/pray/single?ezan=Yats%C4%B1&data.city=istanbul"
response = requests.get(url, headers=headers)
data = response.json()

if data['success']:
    print(data['result'][0]['remainingTime'])


