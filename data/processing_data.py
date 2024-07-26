import numpy as np
import pandas as pd
from copy import deepcopy
from collections import Counter
from datetime import datetime
import json

'''
This class is to preprocess the dataset and generate the dataframe of basic analysis across the elements(units, augments, items)
By making augments, units, and item stacks, the empty dataframes that were generated from 'list_csv' class get updated
The crosscheck does extract the statistics of augments, items, and champions for one specific augment, items, or champions
ex) 'champion_item_crosscheck'  returns the statistics of the list of all items used for a specific champion(define in 'DataBase' file as a varible 'champion')
'''
class basic_preprocessing:

    def __init__(self, game_result, unit_result, cluster_on=False):
        # Initialize class with game_result and unit_result data
        self.game_result = game_result
        self.unit_result = unit_result

        # Load external data from CSV files into DataFrames
        self.augment_list = pd.read_csv('augments_list.csv')
        self.champion_list = pd.read_csv('champs_list.csv')
        self.item_list = pd.read_csv('items_list.csv')

        # Merge game_result and unit_result based on the cluster_on flag
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

        # Apply preprocessing functions
        self.change_gloves_item()
        self.check_item_unit_itemver()

    def change_gloves_item(self):
        '''
        When the unit is equipped with either thief's gloves or accomplice's gloves,
        convert the value of two other item slots to 'None'
        '''
        # Check if item1 is either "Thief's Gloves" or "Accomplice's Gloves"
        check = np.logical_or(self.after_join.item1 == "Thief's Gloves", self.after_join.item1 == "Accomplice's Gloves")

        # Set item2 and item3 to 'None' where the condition is met
        self.after_join.loc[check, 'item2'] = 'None'
        self.after_join.loc[check, 'item3'] = 'None'
        return self.after_join

    def check_item_unit_itemver(self):
        '''
        Count the number of items equipped for each unit
        '''
        check = self.after_join.apply(lambda x: 3 - list(x).count('None'), axis=1)
        self.after_join['num_item'] = check
        after_join = pd.DataFrame(self.after_join)
        after_join.to_csv("afterjoin.csv", sep=',', index=False, encoding='utf-8')

        return self.after_join

    def make_augment_stack(self, game_result, augment_list):
        # Extract relevant columns and drop duplicate rows from 'after_join' DataFrame
        check = game_result[
            ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3']].drop_duplicates()

        # Create a copy of 'augment_list' to store results
        result = augment_list.copy()

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

        # Drop rows where Count is 0 and reset index
        result = result[result['Count'] > 0]
        result = result.drop_duplicates(subset='Name', keep='first')
        result = result.reset_index(drop=True)

        # Save the result DataFrame to a CSV file
        result.to_csv('augment_stack.csv', sep=',', index=False, encoding='utf-8')

        return result

    def make_unit_stack(self, game_result, champion_list):
        # Create a copy of the champion list DataFrame to store results
        result = champion_list.copy()

        # Iterate through each placement, tier, and item count
        for placement in range(1, 9):
            for tier in range(1, 4):
                for num_item in range(1, 4):
                    # Filter rows based on current placement, tier, and item count
                    case = np.logical_and(np.logical_and(game_result.Placement == placement, game_result.tier == tier),
                                          game_result.num_item == num_item)
                    # Extract character_id values for the filtered rows
                    champions = game_result.loc[case, 'character_id'].tolist()
                    champions = Counter(champions)

                    # Update the result DataFrame with the calculated scores for each champion
                    for champion in champions.keys():
                        number = champions[champion]

                        if placement == 1:
                            score = [number, number * placement, number * placement, number * tier, number * tier,
                                     number * tier, number, number, number, number, num_item * number,
                                     num_item * number, num_item * number, num_item * number]

                            if num_item == 3:
                                score += [number] * 4
                            else:
                                score += [0] * 4

                        elif placement <= 4:
                            score = [number, number * placement, number * placement, number * tier, number * tier, 0, 0,
                                     0, number, number, num_item * number, num_item * number, num_item * number, 0]

                            if num_item == 3:
                                score += [number] * 3 + [0]

                            else:
                                score += [0] * 4
                        else:
                            score = [number, number * placement, 0, number * tier, 0, 0, 0, 0, 0, 0, num_item * number,
                                     num_item * number, 0, 0]

                            if num_item == 3:
                                score += [number] * 2 + [0] * 2
                            else:
                                score += [0] * 4

                        result.loc[result.Name == champion, ['Count', 'Ave_score', 'Ave_score_save', 'Ave_star',
                                                             'Ave_star_save', 'Ave_star_win',
                                                             'Win_count', 'Win_rate', 'Save_count', 'Save_rate',
                                                             'Num_items_count', 'Num_items_avg', 'Num_items_save',
                                                             'Num_items_win', 'Full_item_count', 'Full_item_rate',
                                                             'Full_item_save', 'Full_item_win']] += score

        # Calculate average scores, rates, and round them to 1 decimal place
        result.Ave_score = round(result.Ave_score / result.Count, 1)
        result.Ave_score_save = round(result.Ave_score_save / result.Save_count, 1)
        result.Win_rate = round(result.Win_rate / result.Count * 100, 1)
        result.Save_rate = round(result.Save_rate / result.Count * 100, 1)
        result.Ave_star = round(result.Ave_star / result.Count, 1)
        result.Ave_star_save = round
        result.Ave_star_save = round(result.Ave_star_save / result.Save_count, 1)
        result.Ave_star_win = round(result.Ave_star_win / result.Win_count, 1)
        result.Num_items_avg = round(result.Num_items_avg / result.Count, 1)
        result.Num_items_save = round(result.Num_items_save / result.Save_count, 1)
        result.Num_items_win = round(result.Num_items_win / result.Win_count, 1)
        result.Full_item_rate = round(result.Full_item_rate / result.Count * 100, 1)
        result.Full_item_save = round(result.Full_item_save / result.Save_count * 100, 1)
        result.Full_item_win = round(result.Full_item_win / result.Win_count * 100, 1)

        # Save the result DataFrame to a CSV file
        result.to_csv('unit_stack.csv', sep=',', index=False, encoding='utf-8')

        return result

    def make_item_stack(self, game_result, item_list):
        # Create a copy of the item list DataFrame to store results
        result = item_list.copy()

        # Iterate through each placement position from 1 to 8
        for placement in range(1, 9):
            check = game_result.loc[game_result.Placement == placement, :]
            items = check.item1.tolist() + check.item2.tolist() + check.item3.tolist()
            items = Counter(items)

            # Update the result DataFrame with the calculated scores for each item
            for item in items.keys():
                if item == 'None':
                    continue
                else:
                    number = items[item]

                    if placement == 1:
                        item_score = [number, number * placement, number * placement, number, number, number, number]
                    elif placement <= 4:
                        item_score = [number, number * placement, number * placement, 0, 0, number, number]
                    else:
                        item_score = [number, number * placement, 0, 0, 0, 0, 0]

                    result.loc[result.Name == item, ['Count', 'Ave_score', 'Ave_score_save', 'Win_count', 'Win_rate',
                                                     'Save_count', 'Save_rate']] += item_score

        # Calculate average scores, rates, and round them to 1 decimal place
        result.Ave_score = round(result.Ave_score / result.Count, 1)
        result.Ave_score_save = round(result.Ave_score_save / result.Save_count, 1)
        result.Win_rate = round(result.Win_rate / result.Count * 100, 1)
        result.Save_rate = round(result.Save_rate / result.Count * 100, 1)

        # Save the result DataFrame to a CSV file
        result.to_csv('item_stack.csv', sep=',', index=False, encoding='utf-8')

        return result

    def make_stack(self):
        # Generate stacks for augments, units, and items and sort them by 'Count'
        augment_stack = self.make_augment_stack(self.after_join, self.augment_list).sort_values('Count',
                                                                                                ascending=False)
        unit_stack = self.make_unit_stack(self.after_join, self.champion_list).sort_values('Count', ascending=False)
        item_stack = self.make_item_stack(self.after_join, self.item_list).sort_values('Count', ascending=False)

        return augment_stack, unit_stack, item_stack

    def augment_augment_crosscheck(self, augment):
        # Filter rows where any augment matches the given augment
        check = np.logical_or(np.logical_or(self.after_join.augment1 == augment, self.after_join.augment2 == augment),
                              self.after_join.augment3 == augment)
        check = self.after_join[check]

        # Generate and return an augment stack for the filtered data
        check_augment = self.make_augment_stack(check, self.augment_list)

        return check_augment

    def augment_champion_crosscheck(self, augment):
        # Filter rows where any augment matches the given augment
        check = np.logical_or(np.logical_or(self.after_join.augment1 == augment, self.after_join.augment2 == augment),
                              self.after_join.augment3 == augment)
        check = self.after_join[check]

        # Generate and return a unit stack for the filtered data
        check_champion = self.make_unit_stack(check, self.champion_list)

        return check_champion

    def augment_item_crosscheck(self, augment):
        # Filter rows where any augment matches the given augment
        check = np.logical_or(np.logical_or(self.after_join.augment1 == augment, self.after_join.augment2 == augment),
                              self.after_join.augment3 == augment)
        check = self.after_join[check]

        # Generate and return an item stack for the filtered data
        check_item = self.make_item_stack(check, self.item_list)

        return check_item

    def champion_champion_crosscheck(self, champion):
        # Filter rows where character_id matches the given champion
        check = self.after_join.loc[self.after_join.character_id == champion, ['Game_id', 'Player_id']]
        check = pd.merge(self.after_join, check, on=['Game_id', 'Player_id'])

        # Generate and return a unit stack for the filtered data
        check_champion = self.make_unit_stack(check, self.champion_list)

        return check_champion

    def champion_augment_crosscheck(self, champion):
        # Filter rows where character_id matches the given champion
        check = self.after_join.character_id == champion
        check = self.after_join[check]

        # Generate and return an augment stack for the filtered data
        check_augment = self.make_augment_stack(check, self.augment_list)

        return check_augment

    def champion_item_crosscheck(self, champion):
        # Filter rows where character_id matches the given champion
        check = self.after_join.character_id == champion
        check = self.after_join[check]

        # Generate and return an item stack for the filtered data
        check_item = self.make_item_stack(check, self.item_list)

        return check_item

    def item_item_crosscheck(self, item):
        # Filter rows where any item slot matches the given item
        check = np.logical_or(np.logical_or(self.after_join.item1 == item, self.after_join.item2 == item),
                              self.after_join.item3 == item)
        check = self.after_join[check]

        # Generate and return an item stack for the filtered data
        check_item = self.make_item_stack(check, self.item_list)

        return check_item

    def item_augment_crosscheck(self, item):
        # Filter rows where any item slot matches the given item
        check = np.logical_or(np.logical_or(self.after_join.item1 == item, self.after_join.item2 == item),
                              self.after_join.item3 == item)
        check = self.after_join[check]

        # Generate and return an augment stack for the filtered data
        check_augment = self.make_augment_stack(check, self.augment_list)

        return check_augment

    def item_champion_crosscheck(self, item):
        # Filter rows where any item slot matches the given item
        check = np.logical_or(np.logical_or(self.after_join.item1 == item, self.after_join.item2 == item),
                              self.after_join.item3 == item)
        check = self.after_join[check]

        # Generate and return a unit stack for the filtered data
        check_champion = self.make_unit_stack(check, self.champion_list)

        return check_champion
