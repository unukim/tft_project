import pandas as pd
import requests
from src.helpers import get_api_key, is_world_server_valid


class RiotAPI:
    
    def __init__(self):
        """
        Initializes the RIOT class with an API key.
        The API key is retrieved from a file named "key.txt".
        """
        
        self.api_key = get_api_key("key.txt")
        self.world = "europe"


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


    def get_challenger(self):
        #Get the user information of every challenger players
        url = f"https://euw1.api.riotgames.com/tft/league/v1/challenger?queue=RANKED_TFT&api_key={self.api_key}"
        return self.get(url)

    
    def challengers_PUUID(self):
        # storing the puuid of each challenger players from get_challenger() function request
        challengers_puuid = []
        challengers = self.get_challenger()
        summoners_ids = [entry['summonerId'] for entry in challengers['entries'][:5]]

        for summoner_id in summoners_ids:
            url = f"https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/{summoner_id}?api_key={self.api_key}"
            
            try:
                summoner_info = self.get(url)
                
                if not isinstance(summoner_info, list):
                    continue
                    
                for entry in summoner_info:
                    if 'puuid' in entry:
                        challengers_puuid.append(entry['puuid'])
                
                

            except requests.exceptions.RequestException as e:
                print(f"Error fetching puuid for summoner ID {summoner_id}: {e}")


        return challengers_puuid




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

    def get_match_by_puuid(self, game_count):
        """
        Storing every match ID of each players
        """
        all_match_ids = []
        summoner_ids = self.challengers_PUUID()
        
        for summoner_id in summoner_ids:
            url = f"https://{self.world}.api.riotgames.com/tft/match/v1/matches/by-puuid/{summoner_id}/ids?start=0&count={game_count}&api_key={self.api_key}"
            
            try:
                match_id = self.get(url)
                all_match_ids.extend(match_id)  # Add match IDs to the list

            except requests.exceptions.RequestException as e:
                print(f"Error fetching match IDs for summoner ID {summoner_id}: {e}")



        return all_match_ids


 
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

    def game_result_df(self, match_id: str) -> dict | None:
        # Get the dataframe of game results corresponding to each match ID
        game_url = f"https://{self.world}.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={self.api_key}"
        game_result = requests.get(game_url).json()
        game_df = pd.DataFrame(game_result)
        #game_df.to_csv('game.csv', sep=',', index=False, encoding='utf-8')

        return game_df

        
        