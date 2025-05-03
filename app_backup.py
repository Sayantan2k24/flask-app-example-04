import http.client

conn = http.client.HTTPSConnection("crickbuzz-official-apis.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "fc6a622593mshf5b84b89aa8df7dp1a0b41jsncad324878caa",
    'x-rapidapi-host': "crickbuzz-official-apis.p.rapidapi.com"
}

conn.request("GET", "/rankings/team/?formatType=t20&women=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))