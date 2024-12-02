import pandas as pd
import requests
import json
import pprint

# Constantes

data_space_provider = "http://127.0.0.1:1234"
data_space_consumer = "http://127.0.0.1:1235"
api_test = "http://api-test:3000"


catalog_id = ""
dataservice_id = ""
agreement_id = ""
agreement_pid = ""

## Setup Catalog, Dataservice and agreements

### Create a catalog 

payload = {
    "foaf:homepage": "My catalog in Dataspace provider",
    "dct:title": "My catalog in Dataspace provider"
}
headers = {
    "Content-Type": "application/json",
}
url = data_space_provider + "/api/v1/catalogs"
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
response_as_json = response.json()
catalog_id = response_as_json["@id"]

pprint.pprint(response.json())

### Create a data service 

payload = {
    "dcat:endpointURL": api_test
}
headers = {
    "Content-Type": "application/json",
}
url = data_space_provider + "/api/v1/catalogs/" + catalog_id + "/data-services"
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
response_as_json = response.json()
dataservice_id = response_as_json["@id"]

pprint.pprint(response.json())


### Create an agreement 

payload = {
    "dataServiceId": dataservice_id
}
headers = {
    "Content-Type": "application/json",
}
url = data_space_provider + "/api/v1/agreements"
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
response_as_json = response.json()
agreement_id = response_as_json["agreement_id"]
agreement_pid = "urn:uuid:" + agreement_id

pprint.pprint(response.json())

# Setup transfer

url = data_space_consumer + "/api/v1/setup-transfer"

payload = ""
headers = {}
response = requests.request("POST", url, headers=headers, data=payload)
callbackAddress = response.json()["callbackAddress"]
callbackId = response.json()["callbackId"]
consumerPid = response.json()["consumerPid"]

pprint.pprint(response.json())

# Request transfer

url = data_space_consumer + "/api/v1/request-transfer"

payload = json.dumps({
  "agreementId": agreement_pid,
  "format": "http+pull",
  "dataAddress": None,
  "callbackAddress": callbackAddress,
  "callbackId": callbackId,
  "consumerPid": consumerPid
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.json())


# HTTP: Get data plane address 

import requests

consumerPidUuid = consumerPid.replace("urn:uuid:", "")
url = data_space_consumer + "/api/v1/data-address/" + consumerPidUuid

payload = ""
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)
dataPlaneAddress = response.json()["dataPlaneAddress"]

pprint.pprint(response.json())

# HTTP: use data plane address to get data from the data plane

url = dataPlaneAddress
url = url.replace("ds-consumer", "127.0.0.1")
df = pd.read_json(url + "/comments")
df

# HTTP: suspend transfer

url = data_space_consumer + "/api/v1/suspend-transfer"

payload = json.dumps({
  "consumerPid": consumerPid
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.json())

# HTTP: restart transfer

url = data_space_consumer + "/api/v1/restart-transfer"

payload = json.dumps({
  "consumerPid": consumerPid
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.json())

# HTTP: complete transfer

url = data_space_consumer + "/api/v1/complete-transfer"

payload = json.dumps({
  "consumerPid": consumerPid
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.json())

# Protocol state cannot change

url = data_space_consumer + "/api/v1/restart-transfer"

payload = json.dumps({
  "consumerPid": consumerPid
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

pprint.pprint(response.json())