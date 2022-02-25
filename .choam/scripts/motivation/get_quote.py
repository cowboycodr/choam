import requests

url = "https://zenquotes.io/api/random"

response = requests.request("GET", url).json()[0]["q"]

# Favorite: Your happiness is what truly matters most. Do what you have to do in order to be happy.

print()
print(f"\t{response}\n")