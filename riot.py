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
        self.riot_url = "https://europe.api.riotgames.com/riot/"

    
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

    def get_gameID_bysummoner(self, game_name, tag_line, world, game_count):

        url = self.riot_url + f"account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key=" + self.api_key
        game_url = f"https://{world}.api.riotgames.com/tft/"

        try:
            response = requests.get(url)
        # Check if the request was successful
            if response.status_code == 200:
                puuid = response.json()['puuid']
                game_ids = requests.get(f"{game_url}match/v1/matches/by-puuid/{puuid}/ids?count={game_count}&api_key={self.api_key}").json()
                print(game_ids)
                return game_ids
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error executing API request: {e}")
        
    def get_gameResult(self,world,game_id):
        base_url = f"https://{world}.api.riotgames.com/tft/"
        game_result_code_name = f"match/v1/matches/{game_id}"
        game_url = f"{base_url}{game_result_code_name}?api_key={self.api_key}"

        try:
            response = requests.get(game_url)

        # Check if the request was successful
            if response.status_code == 200:
                game_result = requests.get(game_url).json()
                print(game_result)
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error executing API request: {e}")