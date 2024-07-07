import requests

from helpers import get_api_key


class RIOT:
    def __init__(self):
        """
        Initializes the RIOT class with an API key and the base URL for the Riot Games API.
        The API key is retrieved from a file named "key.txt".
        """
        
        self.api_key = get_api_key("key.txt")
        self.base_url = "https://vn2.api.riotgames.com/tft/"


    
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