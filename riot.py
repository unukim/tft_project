import requests

from helpers import get_api_key


class RIOT:
    def __init__(self):
        self.api_key = get_api_key("key.txt")
        self.base_url = "https://vn2.api.riotgames.com/tft/"


    
    def getLeague(self, queue):
        url = self.base_url + f"league/v1/challenger?queue={queue}&api_key=" + self.api_key
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(data)
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        
        except Exception as e:
            print(f"Error executed API request {e}")