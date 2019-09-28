print("Hello World")
import requests
import json
API_KEY = str("mFbi6aZ8dE6a5j3dKkZ3m8BXFsBXINFX")
req = requests.get("http://api.giphy.com/v1/gifs/search?",{"api_key":API_KEY,"q":"cheeseburgers"})


