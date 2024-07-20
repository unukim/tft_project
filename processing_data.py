import numpy as np
import pandas as pd
from copy import deepcopy
from collections import Counter
from datetime import datetime
import json


class basic_preprocessing:

    def __init__(self, game_result, unit_result, cluster_on=False):

        self.game_result = game_result
        self.unit_result = unit_result
        self.augment_list = pd.read_csv('augments_list.csv')
        self.champion_list = pd.read_csv('champs_list.csv')
        self.item_result = pd.read_csv('items_list.csv')

        if not cluster_on:
            self.after_join = pd.merge(self.unit_result, self.game_result[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3']],
                                       on=['Game_id', 'Player_id', 'Datetime'])
            self.after_join = self.after_join[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3', 'character_id',
                 'rarity', 'tier', 'item1', 'item2', 'item3']]
        else:
            self.after_join = pd.merge(self.unit_result, self.game_result[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3', 'Deck']],
                                       on=['Game_id', 'Player_id', 'Datetime'])
            self.after_join = self.after_join[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'Deck', 'augment1', 'augment2', 'augment3',
                 'character_id', 'rarity', 'tier', 'item1', 'item2', 'item3']]

    #When the unit is equipped with either thief's gloves or accomplice's gloves, convert the value of two other item slots to 'None'
    def change_gloves_item(self):

        check = np.logical_or(self.after_join.item1 == "Thief's Gloves", self.after_join.item1 == "Accomplice's Gloves")

        self.after_join.loc[check, 'item2'] = 'None'

        self.after_join.loc[check, 'item3'] = 'None'
        return self.after_join


    #Count the number of items that are equipped for each unit
    def check_item_unit_itemver(self):

        check = self.after_join.apply(lambda x: 3 - list(x).count('None'), axis=1)

        self.after_join['num_item'] = check
        after_join = pd.DataFrame(self.after_join)
        after_join.to_csv("afterjoin.csv", sep=',', index=False, encoding='utf-8')

        return self.after_join
    def make_augment_stack(self):
        # Extract relevant columns and drop duplicate rows from 'after_join' DataFrame
        check = self.after_join[
            ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3']].drop_duplicates()

        # Create a copy of 'augment_list' to store results
        result = self.augment_list.copy()

        # Iterate through each placement position from 1 to 8
        for i in range(1, 9):
            # Filter rows where Placement equals the current position 'i'
            place = check[check.Placement == i]

            # Collect all augment values from augment1, augment2, and augment3 columns
            augments = place[['augment1', 'augment2', 'augment3']].values.flatten()

            # Count occurrences of each augment
            augment_counts = Counter(augments)

            # Calculate scores for each augment based on their count and placement
            for augment, number in augment_counts.items():
                if augment:  # Skip empty augment strings
                    if i == 1:
                        augment_score = [number, number * i, number * i, number, number, number, number]
                    elif i <= 4:
                        augment_score = [number, number * i, number * i, 0, 0, number, number]
                    else:
                        augment_score = [number, number * i, 0, 0, 0, 0, 0]

                    # Update the result DataFrame with the calculated scores
                    result.loc[result.Name == augment,
                    ['Count', 'Ave_score', 'Ave_score_save', 'Win_count', 'Win_rate', 'Save_count',
                     'Save_rate']] += augment_score

        # Avoid division by zero
        result['Ave_score'] = result['Ave_score'] / result['Count'].replace(0, 1)
        result['Ave_score_save'] = result['Ave_score_save'] / result['Save_count'].replace(0, 1)
        result['Win_rate'] = (result['Win_rate'] / result['Count'].replace(0, 1)) * 100
        result['Save_rate'] = (result['Save_rate'] / result['Count'].replace(0, 1)) * 100

        # Round to 1 decimal place
        result['Ave_score'] = result['Ave_score'].round(1)
        result['Ave_score_save'] = result['Ave_score_save'].round(1)
        result['Win_rate'] = result['Win_rate'].round(1)
        result['Save_rate'] = result['Save_rate'].round(1)
        # Drop rows where Count is 0
        result = result[result['Count'] > 0]
        result = result.drop_duplicates(subset='Name', keep='first')
        # Reset the index of the result DataFrame
        result = result.reset_index(drop=True)

        # Save the result DataFrame to a CSV file
        result.to_csv('augment.csv', sep=',', index=False, encoding='utf-8')

        return result
