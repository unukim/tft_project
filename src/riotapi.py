import requests

from src.helpers import get_api_key, is_world_server_valid


class RiotAPI:
    
    def __init__(self):
        """
        Initializes the RIOT class with an API key.
        The API key is retrieved from a file named "key.txt".
        """
        
        self.api_key = get_api_key("key.txt")


    def get(self, url: str) -> dict|None:
        """
        Makes a GET request to the specified URL and returns the JSON response if successful.

        Parameters:
        url (str): The URL to which the GET request is made.

        Returns:
        dict: A dictionary containing the JSON response if the request is successful, or None if it fails.
        """
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to retrieve data: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error executing API request: {e}")
            return None


    def get_gameID_bysummoner(self, game_name: str, tag_line: str, world: str, game_count: int) -> list:
        """
        Retrieves game IDs by summoner information from the Riot Games API.

        Parameters:
        
        game_name (str): The summoner's game name.
        tag_line (str): The summoner's tag line.
        world (str): The server region (e.g., "america", "asia", "europe", "sea").
        game_count (int): The number of recent games to retrieve.

        Returns:
        list: A list of game IDs if the request is successful. The game IDs list will be reversed,
            the newest game will be placed at the last items in the list.
        None: Returns None if the server region is invalid or if there is an error in the API request.
        """
        
        if not is_world_server_valid(world):
            return None
        
        url = f"https://{world}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={self.api_key}"
        
        response = self.get(url)
        
        if response:
            
            puuid = response['puuid']
            game_ids_url = f"https://{world}.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?count={game_count}&api_key={self.api_key}"
            return self.get(game_ids_url)
            
        else:
            return None

 
    def get_game_result(self, world: str, game_id: str) -> dict|None:
            """
            Retrieves the game result for a specific game ID from the Riot Games API.

            Parameters:
            world (str): The server region (e.g., "america", "asia", "europe", "sea").
            game_id (str): The unique identifier of the game.

            Returns:
            dict: A dictionary containing the game result if the request is successful.
            None: Returns None if the server region is invalid or if there is an error in the API request.
            """
            
            if not is_world_server_valid(world):
                return None

            game_url = f"https://{world}.api.riotgames.com/tft/match/v1/matches/{game_id}?api_key={self.api_key}"
            

            return self.get(game_url)

