from src.riotapi import RiotAPI
from game_df import make_df
from processing_data import basic_preprocessing
from list_csv import make_list_df
import json
import pandas as pd

if __name__ == "__main__":

    file_path = 'data/data_dragon.json'
    with open(file_path, "r") as json_file:
        data_dragon = json.load(json_file)

    list = make_list_df(data_dragon)
    list.make_item_list()
    list.make_augment_list()
    list.make_champ_list()

    riot_api = RiotAPI()
    game_count = '1'
    game_ids = riot_api.get_match_by_puuid()

    all_game_results = []
    all_unit_results = []

    for game_id in game_ids:
        game_result = riot_api.game_result_df(game_id)
        game_result_data = make_df(game_result, '5', data_dragon)

        game_result_df = game_result_data.make_new_game_result()
        unit_result_df = game_result_data.make_unit_result()
        all_game_results.append(game_result_df)
        all_unit_results.append(unit_result_df)

    combined_game_results = pd.concat(all_game_results, ignore_index=True)
    combined_unit_results = pd.concat(all_unit_results, ignore_index=True)
    print(combined_game_results)

    preprocessed_data = basic_preprocessing(combined_game_results, combined_unit_results)
    print(preprocessed_data.make_augment_stack())



