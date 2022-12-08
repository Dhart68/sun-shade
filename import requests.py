import requests

url = "https://dark-sky.p.rapidapi.com/37.774929,-122.419418,2019-02-20"

headers = {
	"X-RapidAPI-Key": "b33dad67d0msha31fb1e52c63056p115d00jsne88b161798f3",
	"X-RapidAPI-Host": "dark-sky.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
