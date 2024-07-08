import requests
import pandas as pd

from helpers import get_api_key


class RIOT:
    def __init__(self):
        """
        Initializes the RIOT class with an API key and the base URL for the Riot Games API.
        The API key is retrieved from a file named "key.txt".
        """
        
        self.api_key = get_api_key("key.txt")
        self.base_url = "https://euw1.api.riotgames.com/tft/"

        self.request_header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://developer.riotgames.com",
            "X-Riot-Token": self.api_key
        }


    
    def getLeague(self, queue = "RANKED_TFT"):
        """
        Retrieves the league data for a given queue from the Riot Games API.

        Parameters:
        queue (str): The queue type (e.g., default to "RANKED_TFT") for which to retrieve league data.

        Returns:
        None. Prints the retrieved data if the request is successful, or an error message if it fails.
        """

        url = self.base_url + f"league/v1/challenger?queue={queue}&api_key=" + self.api_key
        try:
            print(url)
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                print(data)
                
                #CREATE THE TABLE BASED ON THE ENTRIES
                challenger_df = pd.DataFrame(data['entries'])
                print(challenger_df)
                challenger_df.to_csv('challenger.csv', sep=',', index=False, encoding='utf-8')
                
            else:
                print(f"Failed to retrieve data: {response.status_code}")
        
        except Exception as e:
            print(f"Error executed API request {e}")

    def get(self, url):
        """
        Makes a GET request to the specified URL and prints the retrieved data if the request is successful.

        Parameters:
        url (str): The URL to which the GET request is made.

        Returns:
        None. Prints the retrieved data if the request is successful, or an error message if it fails.
        """

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(f"Failed to retrieve data: {response.status_code}")

    def extract_game_by_summoner(self, id_name):

        id_url = self.base_url+f"summoner/v1/summoners/by-name/{id_name}"
        my_id = requests.get(id_url, headers=self.request_header).json()

        print(my_id)


       
