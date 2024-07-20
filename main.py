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

    #Create empty dataframe(csv file) structure of each game elements
    list = make_list_df(data_dragon)
    list.make_item_list()
    list.make_augment_list()
    list.make_champ_list()

    riot_api = RiotAPI()
    game_count = '1'
    match_ids = riot_api.get_match_by_puuid(game_count)

    #Store processed game results and unit results of every match
    all_game_results = []
    all_unit_results = []

    for match_id in match_ids:
        game_result = riot_api.game_result_df(match_id)
        # Process raw game dataset and Create the new dataframe
        game_result_data = make_df(game_result, '5', data_dragon)
        game_result_df = game_result_data.make_new_game_result()
        unit_result_df = game_result_data.make_unit_result()

        #Append new game results for each match
        all_game_results.append(game_result_df)
        all_unit_results.append(unit_result_df)

    #Combine the game results into one dataframe
    combined_game_results = pd.concat(all_game_results, ignore_index=True)
    combined_unit_results = pd.concat(all_unit_results, ignore_index=True)

    # Drop duplicate rows with the same game date, player, and game
    combined_game_results = combined_game_results.drop_duplicates(subset=['Datetime', 'Player_id', 'Game_id'])
    combined_unit_results = combined_unit_results.drop_duplicates(subset=['Datetime', 'Player_id', 'Game_id'])

    combined_game_results.to_csv('game_result.csv', sep=',', index=False, encoding='utf-8')
    combined_unit_results.to_csv('unit_result.csv', sep=',', index=False, encoding='utf-8')

    preprocessed_data = basic_preprocessing(combined_game_results, combined_unit_results)
    print(preprocessed_data.make_augment_stack())



