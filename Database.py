from src.riotapi import RiotAPI

from data.game_df import make_df
from data.processing_data import basic_preprocessing
from data.list_csv import make_list_df

import json
import pandas as pd
import os


class DatabaseAPI:
    """High Level API for retrieving database
    """

    def __init__(self) -> None:
        pass

    def main(self):

        file_path = 'data/data_dragon.json'
        with open(file_path, "r") as json_file:
            data_dragon = json.load(json_file)

        list = make_list_df(data_dragon)
        list.make_item_list()
        list.make_augment_list()
        list.make_champ_list()

        riot_api = RiotAPI()
        game_count = '5'
        match_ids = riot_api.get_match_by_puuid(game_count)

        all_game_results = []
        all_unit_results = []

        for match_id in match_ids:
            game_result = riot_api.game_result_df(match_id)
            game_result_data = make_df(game_result, '5', data_dragon)
            game_result_df = game_result_data.make_new_game_result()
            unit_result_df = game_result_data.make_unit_result()

            all_game_results.append(game_result_df)
            all_unit_results.append(unit_result_df)

        combined_game_results = pd.concat(all_game_results, ignore_index=True)
        combined_unit_results = pd.concat(all_unit_results, ignore_index=True)

        existing_game_results = pd.read_csv('game_result.csv')
        combined_game_results = pd.concat([existing_game_results, combined_game_results], ignore_index=True)


        existing_unit_results = pd.read_csv('unit_result.csv')
        combined_unit_results = pd.concat([existing_unit_results, combined_unit_results], ignore_index=True)

        combined_game_results = combined_game_results.drop_duplicates(subset=['Datetime', 'Player_id', 'Game_id'])
        combined_unit_results = combined_unit_results.drop_duplicates(
            subset=['Datetime', 'Player_id', 'Game_id', 'character_id'])

        combined_game_results.to_csv('game_result.csv', sep=',', index=False, encoding='utf-8')
        combined_unit_results.to_csv('unit_result.csv', sep=',', index=False, encoding='utf-8')

        preprocessed_data = basic_preprocessing(combined_game_results, combined_unit_results)
        augment = 'New Recruit'
        champion = 'Sylas'
        item = 'Redemption'

        augment_champion = pd.DataFrame(preprocessed_data.augment_champion_crosscheck(augment))
        augment_champion.to_csv('aug_cham.csv', sep=',', index=False, encoding='utf-8')

        champion_champion = pd.DataFrame(preprocessed_data.champion_champion_crosscheck(f'TFT11_{champion}'))
        champion_champion.to_csv('cham_cham.csv', sep=',', index=False, encoding='utf-8')

        item_champion = pd.DataFrame(preprocessed_data.item_champion_crosscheck(item))
        item_champion.to_csv('item_cham.csv', sep=',', index=False, encoding='utf-8')

        preprocessed_data.make_stack()


