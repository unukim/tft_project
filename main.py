from src.riotapi import RiotAPI
from game_df import make_df
import json

if __name__ == "__main__":

    file_path = 'data/data_dragon.json'
    with open(file_path, "r") as json_file:
        data_dragon = json.load(json_file)

    riot_api = RiotAPI()
    game_name = "sowieso"
    tag_line = "1116"
    game_count = 1
    region = "europe"
    
    game_ids = riot_api.get_gameID_bysummoner(game_name, tag_line, region, game_count)
    print("Fetched Game IDs:", game_ids)

    game_result = riot_api.game_result_df(region, game_ids[0])

    game_result_data = make_df(game_result, 5, data_dragon)

    game_result_data.make_new_game_result()