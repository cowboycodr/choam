import requests

url = "https://zenquotes.io/api/random"

response = requests.request("GET", url).json()[0]["q"]

print()
print(f"\t{response}\n")