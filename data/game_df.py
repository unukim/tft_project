from src.riotapi import RiotAPI
import numpy as np
import pandas as pd
import json
from datetime import datetime

'''
Class for creating the dataframe that stores the statistics of the match 
add_augment_columns : Store the list of augments into 3 seperate columns
make_trait_dataframe: Create 'trait' dataframe that contains the related information, will be added into total game summary dataframe as a seperate column
make_unit_dataframe: Create 'unit' datafame that contains the related information,  will be added into total game summary dataframe as a seperate column
make_new_game_result : Create the game summary dataframe that contains every necessary match data of each participant 
make_trait_result: Return the csv file that only includes the player's 'trait' data
make_unit_result: Return the csv file that only includes the player's 'unit' data
'''
class make_df:

    def __init__(self, df, version, data_dragon):
        self.df = df
        self.version = version
        self.data_dragon = data_dragon
        self.item_data = pd.DataFrame(self.data_dragon['items'])
        self.champ = pd.DataFrame(pd.DataFrame(self.data_dragon['setData']).iloc[2, 0])
        self.game_id = self.df['metadata']['match_id']
        self.game_result = pd.DataFrame(self.df['info']['participants']).drop(['companion'], axis=1)
        self.game_result['game_id'] = self.game_id
        self.game_result = self.game_result[
            ['game_id', 'puuid', 'placement', 'level', 'gold_left', 'last_round', 'time_eliminated',
             'total_damage_to_players', 'augments', 'traits', 'units']]
        self.champ_name = {self.champ.apiName[i] : self.champ.name[i] for i in range(self.champ.shape[0])}
        self.date = str(datetime.fromtimestamp(int(self.df['info']['game_datetime']) / 1000)).split(' ')[0]


# Adding 3 new columns for each augments
    def add_augment_columns(self):
        change_results = []

        for augments in self.game_result['augments']:
            change_result = []

            for augment in augments:
                change_augment = self.item_data.loc[self.item_data.apiName == augment, 'name'].values[0]
                change_result.append(change_augment)

            length_change_result = len(change_result)

            if length_change_result < 3:
                change_result = change_result + ['None'] * (3 - length_change_result)

            change_results.append(change_result)

        change_results = pd.DataFrame(change_results, columns=['augment1', 'augment2', 'augment3'])

        self.game_result[['augment1', 'augment2', 'augment3']] = change_results
        self.game_result = self.game_result[['game_id', 'puuid', 'placement', 'level', 'gold_left',
                                             'last_round', 'time_eliminated', 'total_damage_to_players',
                                             'augment1', 'augment2', 'augment3', 'traits', 'units']]

        return self.game_result
    def make_trait_dataframe(self, trait):
        trait = pd.DataFrame(trait)
        # Check if the trait dataframe is empty
        if trait.shape[0] == 0:
            return pd.DataFrame(columns=['name', 'num_units', 'tier_current', 'tier_total'])

        trait = trait[trait.tier_current != 0].drop(['style'], axis=1).reset_index(drop=True)
     
        return trait

    def make_unit_dataframe(self, unit):
        try:
            units = pd.DataFrame(unit)
            if units.shape[0] == 0:
                return pd.DataFrame(
                    columns=['character_id', 'rarity', 'tier', 'items', 'item1', 'item2', 'item3'])

            item_list = []
            champ_name = []

            for i in range(len(units['character_id'])):
                character_id = units['character_id'][i]
                if character_id in self.champ_name:
                    champ_name.append(self.champ_name[character_id])
                    check = units['itemNames'][i]
                    check += [0] * (3 - len(check))
                    item_list.append(check)
            units['items'] = item_list

            item1 = []
            item2 = []
            item3 = []

            for item in item_list:
                check_item = []
                for i in item:
                    if i == 0:
                        check_item.append('None')
                    else:
                        item_name = self.item_data.loc[self.item_data.apiName == i, 'name'].values[0]
                        check_item.append(item_name)
                item1.append(check_item[0])
                item2.append(check_item[1])
                item3.append(check_item[2])

            units = pd.DataFrame(unit).drop(['itemNames'], axis=1)
            units['item1'] = item1
            units['item2'] = item2
            units['item3'] = item3
            units.character_id = list(map(lambda x: x.replace(self.version, ''), units.character_id))
            units['champ_name'] = champ_name

            return units

         #Skip if the function makes the error, it for some reasons often detects some cases with index error. Could not find where the issues are cause.
        except Exception as e:
            print(f"Error in make_unit_dataframe: {e}")
            return pd.DataFrame(columns=['character_id', 'rarity', 'tier', 'items', 'item1', 'item2', 'item3'])

    def make_new_game_result(self):
        self.add_augment_columns()
        #Initiate the column for all necessary dataset
        New_result = {'Datetime': self.date,
                      'Game_id': self.df['metadata']['match_id'],
                      'Player_id': [],
                      'Placement': [],
                      'Time': [],
                      'Last_round': [],
                      "Damage_player": [],
                      "Gold_left": [],
                      "augment1": [],
                      'augment2': [],
                      'augment3': [],
                      "traits": [],
                      "num_units": [],
                      "tier_current": [],
                      "units": [],
                      "unit_tier": [],
                      "item_name": []}

        New_result['Player_id'] += (list(self.game_result.puuid))

        New_result['Placement'] += (list(self.game_result.placement))

        New_result['Time'] += (list(self.game_result.time_eliminated))

        New_result['Last_round'] += (list(self.game_result.last_round))

        New_result['Damage_player'] += (list(self.game_result.total_damage_to_players))

        New_result['Gold_left'] += (list(self.game_result.gold_left))

        New_result['augment1'] += list(self.game_result.augment1)

        New_result['augment2'] += list(self.game_result.augment2)

        New_result['augment3'] += list(self.game_result.augment3)

        #Append the dataframe for each player in the game
        for player in range(self.game_result.shape[0]):
            trait_dataframe = pd.DataFrame(self.game_result.loc[player, 'traits'])
            trait_dataframe = self.make_trait_dataframe(trait_dataframe)

            New_result['traits'].append(list(trait_dataframe.name))
            New_result['num_units'].append(list(trait_dataframe.num_units))
            New_result['tier_current'].append(list(trait_dataframe.tier_current))

            unit_dataframe = self.make_unit_dataframe(self.game_result.loc[player, 'units'])

            New_result['units'].append(list(unit_dataframe.character_id))
            New_result['unit_tier'].append(list(unit_dataframe.tier))
            New_result['item_name'].append(np.array(unit_dataframe.loc[:, ['item1', 'item2', 'item3']]).tolist())

        New_result = pd.DataFrame(New_result)
        New_result.to_csv('game_result.csv', sep=',', index=False, encoding='utf-8')

        return New_result

    def make_trait_result(self, number):

        trait1 = self.make_trait_dataframe(self.game_result.loc[number, 'traits'])
        trait1['Datetime'] = self.date
        trait1['Game_id'] = self.game_id
        trait1['Player_id'] = self.game_result.loc[number, 'puuid']
        trait1 = trait1[
            ['Datetime', 'Game_id', 'Player_id', 'name', 'num_units', 'tier_current', 'tier_total']]
        #trait1.to_csv('trait_result.csv', sep=',', index=False, encoding='utf-8')
        return trait1

    def make_unit_result(self):

        all_units = []

        for number in range(len(self.game_result)):
            unit = self.make_unit_dataframe(self.game_result.loc[number, 'units'])
            unit['Datetime'] = self.date
            unit['Game_id'] = self.game_id
            unit['Player_id'] = self.game_result.loc[number, 'puuid']
            unit = unit[
                ['Datetime', 'Game_id', 'Player_id', 'character_id', 'rarity', 'tier', 'item1', 'item2',
                 'item3']]
            all_units.append(unit)

        # Concatenate all DataFrames into one
        all_units_df = pd.concat(all_units, ignore_index=True)

        # Save to CSV
        all_units_df.to_csv('unit_result.csv', sep=',', index=False, encoding='utf-8')

        return all_units_df


